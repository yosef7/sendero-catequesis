"""Adaptador Ollama. Recibe únicamente estados y cantidades, sin texto libre personal."""
import json
from urllib.request import Request, urlopen
from urllib.error import URLError
from flask import current_app


def evidence_for(record):
    return {
        'etapa_ordinal': record['level_id'],
        'requisitos': [{'numero': i + 1, 'cumplido': bool(r['completed_at'])} for i, r in enumerate(record['requirements'])],
        'clases_registradas': len(record['attendance']),
        'asistencias': sum(r['present'] for r in record['attendance']),
        'hay_siguiente_etapa': bool(record['next_level']),
    }


def generate_plan(record):
    """Propuesta de encuentro, separada de los hechos y de las decisiones."""
    evidence = evidence_for(record)
    pending = [r['numero'] for r in evidence['requisitos'] if not r['cumplido']]
    choices = [
        'Revisar con la catequista el registro de asistencia antes del próximo encuentro.',
        'Preparar una pregunta para conversar con el responsable sobre el acompañamiento.',
        'Registrar una observación de la catequista después del próximo encuentro.',
    ]
    if not evidence['clases_registradas']:
        choices.append('Preparar el registro de la primera clase y su asistencia.')
    else:
        choices.append('Revisar con el responsable si necesita apoyo para la asistencia a las clases.')
    if pending:
        choices.append('Revisar las evidencias de los requisitos pendientes antes de marcarlos como cumplidos.')
    elif evidence['requisitos']:
        choices.append('Revisar con la catequista las evidencias de los requisitos verificados antes de considerar un avance.')
    else:
        choices.append('Confirmar con la catequista los requisitos que corresponden a esta etapa.')
    questions = [
        '¿Qué apoyo necesitan para acompañar la formación entre los encuentros?',
        '¿Hay algo que debamos tener en cuenta para facilitar la asistencia a las clases?',
        '¿Qué les gustaría conversar con la catequista sobre el próximo encuentro?',
    ]
    schema = {'type': 'object', 'properties': {
        'preparation': {'type': 'array', 'items': {'type': 'string', 'enum': choices}, 'minItems': 2, 'maxItems': 3, 'uniqueItems': True},
        'family_question': {'type': 'string', 'enum': questions}}, 'required': ['preparation', 'family_question'], 'additionalProperties': False}
    payload = {'model': current_app.config['OLLAMA_MODEL'], 'stream': False, 'format': schema,
               'options': {'temperature': 0, 'num_predict': 350}, 'messages': [
        {'role': 'system', 'content': 'Prioriza la preparación de una catequista para su próximo encuentro. Devuelve JSON: preparation contiene 2 o 3 acciones distintas, copiadas exactamente de acciones_permitidas y ordenadas por prioridad; family_question contiene una pregunta copiada exactamente de preguntas_permitidas. Si no hay clases, prioriza preparar la primera; si hay requisitos pendientes, prioriza revisar sus evidencias; si todos están verificados, prioriza su revisión humana. Luego considera asistencia y conversación con el responsable. No apruebes ni modifiques requisitos o etapas. No generes texto fuera del catálogo.'},
        {'role': 'user', 'content': json.dumps({'registro': evidence, 'acciones_permitidas': choices, 'preguntas_permitidas': questions}, ensure_ascii=False)}]}
    req = Request('http://127.0.0.1:11434/api/chat', data=json.dumps(payload).encode(), headers={'Content-Type': 'application/json'})
    try:
        with urlopen(req, timeout=120) as response:
            generated = json.loads(json.load(response)['message']['content'])
        if not isinstance(generated, dict) or set(generated) != {'preparation', 'family_question'}:
            return None
        steps = generated['preparation']
        question = generated['family_question']
        if not isinstance(steps, list) or not 2 <= len(steps) <= 3 or any(not isinstance(v, str) or v not in choices for v in steps) or len(set(steps)) != len(steps):
            return None
        if not isinstance(question, str) or question not in questions:
            return None
        return {'preparation': steps, 'family_question': question, 'pending_numbers': pending,
                'model': payload['model'], 'evidence': evidence}
    except (URLError, TimeoutError, ValueError, KeyError, TypeError):
        return None


def summarize(record):
    result = generate_plan(record)
    if result is None:
        return None
    facts=result['evidence']
    return {**result, 'summary': f"{facts['asistencias']} de {facts['clases_registradas']} asistencias. "
            + f"{len(result['pending_numbers'])} requisitos pendientes. " + ' '.join(result['preparation'])}
