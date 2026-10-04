"""Reglas del recorrido; no dependen de la interfaz ni de un modelo de IA."""
from datetime import date, datetime
from zoneinfo import ZoneInfo
import json
import sqlite3
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
    result['guardians'] = [dict(r) for r in db.execute('SELECT * FROM guardians WHERE child_id=? ORDER BY id', (child_id,))]
    result['enrollments'] = [dict(r) for r in db.execute('''SELECT e.*,g.name AS group_name,p.name AS period_name,p.starts,p.ends FROM enrollments e JOIN groups g ON g.id=e.group_id JOIN periods p ON p.id=g.period_id WHERE e.child_id=? ORDER BY e.id DESC''', (child_id,))]
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
    guardians = validate_guardians(data) if 'guardians' in data else None
    group_id = data.get('group_id')
    with db:
        if child_id:
            existing = child(child_id)
            if 'guardian' not in data:
                guardian = existing['guardian']
            if 'contact' not in data:
                contact = existing['contact']
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
        if guardians is not None:
            db.execute('DELETE FROM guardians WHERE child_id=?', (child_id,))
            for g in guardians:
                db.execute('INSERT INTO guardians(child_id,name,relationship,contact) VALUES (?,?,?,?)', (child_id,g['name'],g['relationship'],g['contact']))
            first = guardians[0] if guardians else {'name':'','contact':''}
            db.execute('UPDATE children SET guardian=?,contact=? WHERE id=?', (first['name'],first['contact'],child_id))
        elif 'guardian' in data or 'contact' in data:
            # Keep legacy clients compatible without discarding additional guardians.
            first = db.execute('SELECT id FROM guardians WHERE child_id=? ORDER BY id LIMIT 1',(child_id,)).fetchone()
            if first:
                db.execute('UPDATE guardians SET name=?,contact=? WHERE id=?',(guardian,contact,first['id']))
            elif guardian:
                db.execute('INSERT INTO guardians(child_id,name,contact) VALUES (?,?,?)',(child_id,guardian,contact))
        if group_id is not None:
            enroll(child_id, group_id, joined)
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
        enrollment_id = data.get('enrollment_id')
        if enrollment_id is not None:
            integer(enrollment_id)
            membership = db.execute('''SELECT e.id,e.enrolled,p.starts,p.ends FROM enrollments e JOIN groups g ON g.id=e.group_id JOIN periods p ON p.id=g.period_id WHERE e.id=? AND e.child_id=?''',(enrollment_id,child_id)).fetchone()
            if not membership or not max(membership['starts'],membership['enrolled']) <= day <= membership['ends']:
                raise ValidationError('Selecciona una inscripción propia y una fecha dentro del período.')
        db.execute('''INSERT INTO attendance(child_id,day,topic,present,enrollment_id) VALUES (?,?,?,?,?) ON CONFLICT(child_id,day)
            DO UPDATE SET topic=excluded.topic,present=excluded.present,enrollment_id=excluded.enrollment_id''', (child_id, day, topic, int(present),enrollment_id))
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


def validate_guardians(data):
    values = data.get('guardians')
    if not isinstance(values,list) or len(values)>5:
        raise ValidationError('Registra hasta cinco responsables.')
    result=[]
    for value in values:
        if not isinstance(value,dict):
            raise ValidationError('Responsable inválido.')
        result.append({'name':text(value.get('name'),'Responsable',maximum=120),
                       'relationship':text(value.get('relationship',''),'Vínculo',False,80),
                       'contact':text(value.get('contact',''),'Contacto',False,120)})
    return result


def period_date(value):
    try:
        if date.fromisoformat(value).isoformat()!=value:
            raise ValueError
    except (TypeError,ValueError):
        raise ValidationError('Introduce una fecha válida para el período.')
    return value


def organization():
    db=get_db()
    return {'periods':[dict(r) for r in db.execute('SELECT * FROM periods ORDER BY starts DESC,id DESC')],
            'groups':[dict(r) for r in db.execute('SELECT g.*,p.name AS period_name,p.starts,p.ends FROM groups g JOIN periods p ON p.id=g.period_id ORDER BY p.starts DESC,g.name')]}


def create_period(data):
    name=text(data.get('name'),'Período',maximum=80)
    starts=period_date(data.get('starts')); ends=period_date(data.get('ends'))
    if starts>ends:
        raise ValidationError('El inicio debe ser anterior o igual al cierre.')
    db=get_db()
    try:
        with db:
            db.execute('INSERT INTO periods(name,starts,ends) VALUES (?,?,?)',(name,starts,ends))
    except sqlite3.IntegrityError:
        raise ValidationError('Ya existe un período con ese nombre.')
    return organization()


def create_group(data):
    period_id=integer(data.get('period_id')); name=text(data.get('name'),'Grupo',maximum=80)
    db=get_db()
    if not db.execute('SELECT 1 FROM periods WHERE id=?',(period_id,)).fetchone():
        raise ValidationError('El período no existe.')
    try:
        with db:
            db.execute('INSERT INTO groups(period_id,name) VALUES (?,?)',(period_id,name))
    except sqlite3.IntegrityError:
        raise ValidationError('Ya existe ese grupo en el período.')
    return organization()


def enroll(child_id,group_id,enrolled):
    group_id=integer(group_id); enrolled=valid_date(enrolled)
    db=get_db(); c=active(child_id)
    group=db.execute('SELECT g.*,p.name AS period_name,p.starts,p.ends FROM groups g JOIN periods p ON p.id=g.period_id WHERE g.id=?',(group_id,)).fetchone()
    if not group or not group['starts']<=enrolled<=group['ends'] or enrolled<c['joined']:
        raise ValidationError('La inscripción debe estar dentro del período y no ser anterior al ingreso.')
    if db.execute('SELECT 1 FROM enrollments WHERE child_id=? AND group_id=?',(child_id,group_id)).fetchone():
        raise ValidationError('El participante ya está inscrito en ese grupo.')
    db.execute('INSERT INTO enrollments(child_id,group_id,enrolled) VALUES (?,?,?)',(child_id,group_id,enrolled))
    event(child_id,'Inscripción',f"Inscripción en {group['name']} · {group['period_name']}.",enrolled)
