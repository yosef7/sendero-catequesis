"""Reglas del recorrido; no dependen de la interfaz ni de un modelo de IA."""
from datetime import date, datetime
from zoneinfo import ZoneInfo
import json
from .db import get_db


class ValidationError(Exception):
    pass


def today():
    return datetime.now(ZoneInfo('America/Panama')).date().isoformat()


def text(value, label, required=True, maximum=300):
    if not isinstance(value, str) or len(value.strip()) > maximum:
        raise ValidationError(f'{label}: introduce un texto de hasta {maximum} caracteres.')
    value = value.strip()
    if required and not value:
        raise ValidationError(f'{label} es obligatorio.')
    return value


def valid_date(value):
    try:
        parsed = date.fromisoformat(value)
        if parsed.isoformat() != value or parsed > date.fromisoformat(today()):
            raise ValueError
    except (TypeError, ValueError):
        raise ValidationError('La fecha debe ser válida y no estar en el futuro.')
    return value


def integer(value):
    if type(value) is not int or value < 1:
        raise ValidationError('Selecciona una etapa válida.')
    return value


def event(child_id, kind, detail, day=None):
    get_db().execute('INSERT INTO events(child_id,kind,happened,detail) VALUES (?,?,?,?)',
                     (child_id, kind, day or today(), detail))


def child(child_id):
    row = get_db().execute('SELECT c.*, l.name AS level_name FROM children c JOIN levels l ON l.id=c.level_id WHERE c.id=?', (child_id,)).fetchone()
    if not row:
        raise ValidationError('No se encontró la ficha.')
    return dict(row)


def levels():
    db = get_db()
    return [dict(row, requirements=[dict(r) for r in db.execute('SELECT * FROM requirements WHERE level_id=? ORDER BY id', (row['id'],))])
            for row in db.execute('SELECT * FROM levels ORDER BY position')]


def detail(child_id):
    db = get_db()
    result = child(child_id)
    result['requirements'] = [dict(r) for r in db.execute('''SELECT r.*, c.completed_at FROM requirements r
        LEFT JOIN completions c ON c.requirement_id=r.id AND c.child_id=? WHERE r.level_id=? ORDER BY r.id''', (child_id, result['level_id']))]
    result['events'] = [dict(r) for r in db.execute('SELECT * FROM events WHERE child_id=? ORDER BY happened DESC,id DESC', (child_id,))]
    result['attendance'] = [dict(r) for r in db.execute('SELECT * FROM attendance WHERE child_id=? ORDER BY day DESC', (child_id,))]
    result['all_requirements'] = [dict(r) for r in db.execute('''SELECT r.title,l.name AS level_name,c.completed_at FROM completions c
        JOIN requirements r ON r.id=c.requirement_id JOIN levels l ON l.id=r.level_id WHERE c.child_id=? ORDER BY c.completed_at DESC''', (child_id,))]
    result['next_level'] = next((l for l in levels() if l['position'] > next(x['position'] for x in levels() if x['id'] == result['level_id'])), None)
    from .ai import evidence_for
    result['plans'] = []
    for row in db.execute('SELECT * FROM plans WHERE child_id=? ORDER BY id DESC LIMIT 5', (child_id,)):
        plan = dict(row)
        plan['content'] = json.loads(plan['content'])
        plan['evidence'] = json.loads(plan['evidence'])
        plan['outdated'] = plan['evidence'] != evidence_for(result)
        result['plans'].append(plan)
    return result


def save_child(data, child_id=None):
    name = text(data.get('name'), 'Nombre', maximum=120)
    guardian = text(data.get('guardian', ''), 'Responsable', False, 120)
    contact = text(data.get('contact', ''), 'Contacto', False, 120)
    joined = valid_date(data.get('joined'))
    db = get_db()
    with db:
        if child_id:
            existing = child(child_id)
            if joined != existing['joined']:
                raise ValidationError('La fecha de ingreso se conserva como registro histórico.')
            db.execute('UPDATE children SET name=?,guardian=?,contact=? WHERE id=?', (name, guardian, contact, child_id))
            event(child_id, 'Ficha', 'Se actualizaron los datos de la ficha.')
        else:
            level_id = integer(data.get('level_id'))
            if not db.execute('SELECT 1 FROM levels WHERE id=?', (level_id,)).fetchone():
                raise ValidationError('La etapa no existe.')
            child_id = db.execute('INSERT INTO children(name,guardian,contact,joined,level_id) VALUES (?,?,?,?,?)',
                                  (name, guardian, contact, joined, level_id)).lastrowid
            event(child_id, 'Ingreso', f'Ingreso a {child(child_id)["level_name"]}.', joined)
    return detail(child_id)


def active(child_id):
    result = child(child_id)
    if result['archived']:
        raise ValidationError('Reactiva la ficha para registrar cambios en su formación.')
    return result


def complete(child_id, req_id, completed):
    if type(completed) is not bool:
        raise ValidationError('El estado del requisito debe ser válido.')
    db = get_db()
    with db:
        c = active(child_id)
        req = db.execute('SELECT * FROM requirements WHERE id=? AND level_id=?', (req_id, c['level_id'])).fetchone()
        if not req:
            raise ValidationError('El requisito no pertenece a la etapa actual.')
        exists = db.execute('SELECT 1 FROM completions WHERE child_id=? AND requirement_id=?', (child_id, req_id)).fetchone()
        if bool(exists) != completed:
            if completed:
                db.execute('INSERT INTO completions VALUES (?,?,?)', (child_id, req_id, today()))
            else:
                db.execute('DELETE FROM completions WHERE child_id=? AND requirement_id=?', (child_id, req_id))
            event(child_id, 'Requisito', f'{"Cumplido" if completed else "Marcado pendiente"}: {req["title"]}')
    return detail(child_id)


def promote(child_id, note, expected_level):
    note = text(note, 'Observación', False, 1000)
    db = get_db()
    with db:
        # Serialize validation and transition, including concurrent submissions.
        db.execute('BEGIN IMMEDIATE')
        c = detail(child_id)
        active(child_id)
        if c['level_id'] != integer(expected_level):
            raise ValidationError('La etapa cambió. Actualiza la ficha antes de continuar.')
        if not c['next_level']:
            raise ValidationError('Esta es la última etapa configurada.')
        if not c['requirements'] or any(not r['completed_at'] for r in c['requirements']):
            raise ValidationError('Verifica todos los requisitos antes de cambiar de etapa.')
        db.execute('UPDATE children SET level_id=? WHERE id=?', (c['next_level']['id'], child_id))
        event(child_id, 'Etapa', f'{c["level_name"]} → {c["next_level"]["name"]}. {note}')
    return detail(child_id)


def record_attendance(child_id, data):
    day = valid_date(data.get('day'))
    topic = text(data.get('topic'), 'Tema', maximum=300)
    present = data.get('present')
    if type(present) is not bool:
        raise ValidationError('Selecciona presente o ausente.')
    db = get_db()
    with db:
        c = active(child_id)
        if day < c['joined']:
            raise ValidationError('La clase no puede ser anterior al ingreso.')
        db.execute('''INSERT INTO attendance VALUES (?,?,?,?) ON CONFLICT(child_id,day)
            DO UPDATE SET topic=excluded.topic,present=excluded.present''', (child_id, day, topic, int(present)))
        event(child_id, 'Clase', f'{"Presente" if present else "Ausente"}: {topic}', day)
    return detail(child_id)


def add_note(child_id, data):
    day = valid_date(data.get('day'))
    note = text(data.get('note'), 'Observación', maximum=1000)
    db = get_db()
    with db:
        if day < active(child_id)['joined']:
            raise ValidationError('La observación no puede ser anterior al ingreso.')
        event(child_id, 'Observación', note, day)
    return detail(child_id)
