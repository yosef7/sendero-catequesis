import io
import sqlite3
import json
from flask import Blueprint, request, jsonify, send_file, session
from . import services as s
from .db import get_db
from .ai import summarize, generate_plan

api = Blueprint('api', __name__, url_prefix='/api')


def data():
    result = request.get_json(silent=True)
    if not isinstance(result, dict):
        raise s.ValidationError('Envía un formulario válido.')
    return result


@api.get('/state')
def state():
    children = [s.detail(row['id']) for row in get_db().execute('SELECT id FROM children ORDER BY name COLLATE NOCASE')]
    return jsonify(children=children, levels=s.levels(), today=s.today())


@api.post('/children')
def create():
    return jsonify(s.save_child(data())), 201


@api.patch('/children/<int:child_id>')
def edit(child_id):
    return jsonify(s.save_child(data(), child_id))


@api.put('/children/<int:child_id>/requirements/<int:req_id>')
def requirement(child_id, req_id):
    return jsonify(s.complete(child_id, req_id, data().get('completed')))


@api.post('/children/<int:child_id>/promote')
def promote(child_id):
    body = data()
    return jsonify(s.promote(child_id, body.get('note', ''), body.get('expected_level')))


@api.post('/children/<int:child_id>/attendance')
def attendance(child_id):
    return jsonify(s.record_attendance(child_id, data()))


@api.post('/children/<int:child_id>/notes')
def note(child_id):
    return jsonify(s.add_note(child_id, data()))


@api.post('/children/<int:child_id>/archive')
def archive(child_id):
    archived = data().get('archived')
    if type(archived) is not bool:
        raise s.ValidationError('Selecciona un estado válido.')
    db = get_db()
    with db:
        old = s.child(child_id)
        if bool(old['archived']) != archived:
            db.execute('UPDATE children SET archived=? WHERE id=?', (int(archived), child_id))
            s.event(child_id, 'Ficha', 'Ficha archivada.' if archived else 'Ficha reactivada.')
    return jsonify(s.detail(child_id))


@api.post('/levels')
def add_level():
    name = s.text(data().get('name'), 'Etapa', maximum=80)
    db = get_db()
    try:
        with db:
            db.execute('INSERT INTO levels(name,position) SELECT ?, COALESCE(MAX(position),0)+1 FROM levels', (name,))
    except sqlite3.IntegrityError:
        raise s.ValidationError('Ya existe una etapa con ese nombre.')
    return jsonify(levels=s.levels()), 201


@api.patch('/levels/<int:level_id>')
def rename_level(level_id):
    name = s.text(data().get('name'), 'Etapa', maximum=80)
    db = get_db()
    try:
        with db:
            if db.execute('UPDATE levels SET name=? WHERE id=?', (name, level_id)).rowcount != 1:
                raise s.ValidationError('La etapa no existe.')
    except sqlite3.IntegrityError:
        raise s.ValidationError('Ya existe una etapa con ese nombre.')
    return jsonify(levels=s.levels())


@api.post('/levels/<int:level_id>/requirements')
def add_requirement(level_id):
    title = s.text(data().get('title'), 'Requisito', maximum=200)
    db = get_db()
    if not db.execute('SELECT 1 FROM levels WHERE id=?', (level_id,)).fetchone():
        raise s.ValidationError('La etapa no existe.')
    try:
        with db:
            db.execute('INSERT INTO requirements(level_id,title) VALUES (?,?)', (level_id, title))
    except sqlite3.IntegrityError:
        raise s.ValidationError('Ese requisito ya está registrado.')
    return jsonify(levels=s.levels()), 201


@api.patch('/requirements/<int:req_id>')
def rename_requirement(req_id):
    title = s.text(data().get('title'), 'Requisito', maximum=200)
    db = get_db()
    # Preserve wording of already verified historical requirements.
    if db.execute('SELECT 1 FROM completions WHERE requirement_id=?', (req_id,)).fetchone():
        raise s.ValidationError('Este requisito ya tiene verificaciones. Su texto se conserva como historial.')
    try:
        with db:
            if db.execute('UPDATE requirements SET title=? WHERE id=?', (title, req_id)).rowcount != 1:
                raise s.ValidationError('El requisito no existe.')
    except sqlite3.IntegrityError:
        raise s.ValidationError('Ese requisito ya existe.')
    return jsonify(levels=s.levels())


@api.post('/children/<int:child_id>/summary')
def summary(child_id):
    result = summarize(s.detail(child_id))
    if result is None:
        return jsonify(error='No pudimos conectar con la IA local. Comprueba que Ollama y el modelo estén disponibles. Tu registro sigue funcionando.'), 503
    return jsonify(result)


@api.get('/backup')
def backup():
    destination = sqlite3.connect(':memory:')
    try:
        get_db().backup(destination)
        content = destination.serialize()
    finally:
        destination.close()
    return send_file(io.BytesIO(content), mimetype='application/vnd.sqlite3', as_attachment=True, download_name=f'sendero-respaldo-{s.today()}.sqlite')


@api.post('/children/<int:child_id>/plan')
def plan(child_id):
    s.active(child_id)
    result = generate_plan(s.detail(child_id))
    if result is None:
        return jsonify(error='No se pudo preparar la propuesta. Revisa Ollama y vuelve a intentarlo. No se guardaron cambios.'), 503
    db = get_db()
    with db:
        db.execute('INSERT INTO plans(child_id,level_id,model,evidence,content) VALUES (?,?,?,?,?)',
                   (child_id, result['evidence']['etapa_ordinal'], result['model'], json.dumps(result['evidence']),
                    json.dumps({k: result[k] for k in ('preparation', 'family_question', 'pending_numbers')})))
    return jsonify(s.detail(child_id))


@api.post('/logout')
def logout():
    session.clear()
    return jsonify(ok=True)
