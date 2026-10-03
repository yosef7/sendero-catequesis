import sqlite3
import pytest
from sendero import create_app
from sendero.services import today


@pytest.fixture
def client(tmp_path):
    app = create_app({'TESTING': True, 'DATABASE': str(tmp_path/'test.sqlite'), 'SECRET_KEY':'test', 'ACCESS_CODE':'test-access'})
    client = app.test_client()
    with client.session_transaction() as session:
        session.update(authenticated=True, csrf='test-csrf')
    return client


def send(client, path, body, method='post'):
    return getattr(client, method)('/api'+path, json=body, headers={'X-CSRF-Token':'test-csrf'})


def new_child(client, **changes):
    body={'name':'Niña Ficticia', 'guardian':'Responsable de prueba', 'contact':'contacto privado', 'joined':today(), 'level_id':1}
    body.update(changes)
    result=send(client,'/children',body)
    assert result.status_code == 201
    return result.json


def test_auth_and_csrf(client):
    with client.session_transaction() as session:
        session.clear()
    assert client.get('/api/state').status_code == 401
    assert client.get('/api/backup').status_code == 401
    assert client.post('/api/children',json={}).status_code == 403
    client.get('/login')
    with client.session_transaction() as session:
        csrf=session['csrf']
    assert client.post('/login',data={'csrf':csrf,'code':'wrong'}).status_code == 401
    assert client.post('/login',data={'csrf':csrf,'code':'test-access'}).status_code == 302
    assert client.get('/api/state').status_code == 200


def test_requirements_and_promotion_preserve_history(client):
    c=new_child(client)
    assert send(client,f'/children/{c["id"]}/promote',{'expected_level':1}).status_code == 422
    req=c['requirements'][0]['id']
    checked=send(client,f'/children/{c["id"]}/requirements/{req}',{'completed':True},'put')
    assert checked.status_code == 200
    promoted=send(client,f'/children/{c["id"]}/promote',{'note':'Verificado por la catequista','expected_level':1})
    assert promoted.json['level_id'] == 2
    assert len(promoted.json['all_requirements']) == 1
    assert any(e['kind']=='Etapa' for e in promoted.json['events'])
    assert send(client,f'/children/{c["id"]}/promote',{'expected_level':1}).status_code == 422
    assert send(client,f'/children/{c["id"]}/requirements/{req}',{'completed':False},'put').status_code == 422


def test_attendance_correction_is_audited(client):
    c=new_child(client)
    for present in (True,False):
        response=send(client,f'/children/{c["id"]}/attendance',{'day':today(),'topic':'Clase de prueba','present':present})
        assert response.status_code == 200
    assert len(response.json['attendance']) == 1
    assert response.json['attendance'][0]['present'] == 0
    assert len([e for e in response.json['events'] if e['kind']=='Clase']) == 2


def test_validation_does_not_write(client):
    for changes in ({'name':''},{'joined':'2099-01-01'},{'joined':'2026-02-30'},{'level_id':999},{'level_id':True}):
        body={'name':'Prueba','joined':today(),'level_id':1,**changes}
        assert send(client,'/children',body).status_code == 422
    assert client.get('/api/state').json['children'] == []


def test_archive_is_reversible(client):
    c=new_child(client)
    assert send(client,f'/children/{c["id"]}/archive',{'archived':True}).status_code == 200
    assert send(client,f'/children/{c["id"]}/notes',{'day':today(),'note':'Prueba'}).status_code == 422
    assert send(client,f'/children/{c["id"]}/archive',{'archived':False}).json['archived'] == 0


def test_configuration_and_historical_wording(client):
    assert send(client,'/levels',{'name':'Nueva etapa'}).status_code == 201
    assert send(client,'/levels',{'name':'Nueva etapa'}).status_code == 422
    assert send(client,'/levels/1/requirements',{'title':'Nuevo requisito'}).status_code == 201
    c=new_child(client)
    req=c['requirements'][0]['id']
    send(client,f'/children/{c["id"]}/requirements/{req}',{'completed':True},'put')
    assert send(client,f'/requirements/{req}',{'title':'Texto alterado'},'patch').status_code == 422


def test_backup_is_complete_sqlite(client,tmp_path):
    new_child(client)
    response=client.get('/api/backup')
    assert response.status_code == 200
    backup=tmp_path/'backup.sqlite'
    backup.write_bytes(response.data)
    with sqlite3.connect(backup) as db:
        assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        assert db.execute('SELECT count(*) FROM children').fetchone()[0]==1
        assert db.execute('SELECT count(*) FROM events').fetchone()[0]==1


def test_ai_payload_excludes_personal_fields(client,monkeypatch):
    import sendero.ai as ai
    c=new_child(client)
    captured={}
    class FakeResponse:
        def __enter__(self): return self
        def __exit__(self,*args): pass
        def read(self): return b'{"message":{"content":"Resumen de prueba"}}'
    def fake_urlopen(request,timeout):
        captured['payload']=request.data.decode()
        return FakeResponse()
    monkeypatch.setattr(ai,'urlopen',fake_urlopen)
    response=send(client,f'/children/{c["id"]}/summary',{})
    assert response.status_code==200
    for private in ('Niña Ficticia','Responsable de prueba','contacto privado','Revisión de formación'):
        assert private not in captured['payload']


def test_security_headers_and_host(client):
    response=client.get('/api/state')
    assert response.headers['Cache-Control']=='no-store'
    assert "frame-ancestors 'none'" in response.headers['Content-Security-Policy']
    assert client.get('/api/state',headers={'Host':'untrusted.example'}).status_code == 400


def test_plan_persists_and_detects_changed_evidence(client,monkeypatch):
    from sendero.ai import evidence_for
    import sendero.routes as routes
    c=new_child(client)
    def fake_plan(record):
        return {'preparation':['Revisar pendientes.','Preparar una conversación.'],
                'family_question':'¿Cómo podemos acompañar la formación?', 'pending_numbers':[1],
                'model':'modelo-prueba', 'evidence':evidence_for(record)}
    monkeypatch.setattr(routes,'generate_plan',fake_plan)
    response=send(client,f'/children/{c["id"]}/plan',{})
    assert response.status_code == 200
    plan=response.json['plans'][0]
    assert not plan['outdated']
    assert len(response.json['events']) == 1  # AI never marks a requirement or advances.
    assert response.json['level_id'] == 1
    assert client.get('/api/state').json['children'][0]['plans'][0]['id']==plan['id']
    req=c['requirements'][0]['id']
    changed=send(client,f'/children/{c["id"]}/requirements/{req}',{'completed':True},'put')
    assert changed.json['plans'][0]['outdated']


@pytest.mark.parametrize('output',[None, [], {'preparation':['Solo una'],'family_question':'¿Qué necesitas?'},
                                  {'preparation':[7,'Revisar'],'family_question':'¿Qué necesitas?'},
                                  {'preparation':['Revisar','Conversar'],'family_question':'','extra':'incorrecto'},
                                  {'preparation':['Visitar el domicilio','Inventar una norma'],'family_question':'¿Qué necesitas?'}])
def test_invalid_model_output_does_not_persist(client,monkeypatch,output):
    import sendero.ai as ai
    import json
    c=new_child(client)
    captured={}
    class FakeResponse:
        def __enter__(self): return self
        def __exit__(self,*args): pass
        def read(self): return json.dumps({'message':{'content':json.dumps(output)}}).encode()
    def fake_urlopen(request,timeout):
        captured['payload']=request.data.decode()
        return FakeResponse()
    monkeypatch.setattr(ai,'urlopen',fake_urlopen)
    result=send(client,f'/children/{c["id"]}/plan',{})
    assert result.status_code==503
    assert client.get('/api/state').json['children'][0]['plans']==[]
    for private in ('Niña Ficticia','Responsable de prueba','contacto privado','Revisión de formación'):
        assert private not in captured['payload']


def test_migration_preserves_existing_ficha(tmp_path):
    from pathlib import Path
    database=tmp_path/'version1.sqlite'
    with sqlite3.connect(database) as db:
        db.executescript(Path('sendero/schema.sql').read_text())
        db.execute("INSERT INTO levels VALUES (1,'Etapa real',1)")
        db.execute("INSERT INTO children(name,joined,level_id) VALUES ('Ficha anterior','2026-01-01',1)")
    create_app({'TESTING':True,'DATABASE':str(database)})
    with sqlite3.connect(database) as db:
        assert db.execute('SELECT name FROM children').fetchone()[0]=='Ficha anterior'
        assert db.execute('SELECT MAX(version) FROM schema_version').fetchone()[0]==2
        assert db.execute('SELECT count(*) FROM plans').fetchone()[0]==0


def test_valid_catalog_response_is_accepted(client,monkeypatch):
    import sendero.ai as ai
    import json
    c=new_child(client)
    class FakeResponse:
        def __init__(self,request): self.payload=json.loads(request.data)
        def __enter__(self): return self
        def __exit__(self,*args): pass
        def read(self):
            fields=self.payload['format']['properties']
            result={'preparation':fields['preparation']['items']['enum'][:2],
                    'family_question':fields['family_question']['enum'][0]}
            return json.dumps({'message':{'content':json.dumps(result)}}).encode()
    monkeypatch.setattr(ai,'urlopen',lambda request,timeout:FakeResponse(request))
    result=send(client,f'/children/{c["id"]}/plan',{})
    assert result.status_code==200
    assert len(result.json['plans'][0]['content']['preparation'])==2
