"""Persistencia local: conexiones por solicitud y migraciones versionadas."""
import sqlite3
from pathlib import Path
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'], timeout=10)
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys=ON')
        g.db.execute('PRAGMA journal_mode=WAL')
    return g.db


def initialize():
    db = get_db()
    db.executescript(Path(__file__).with_name('schema.sql').read_text())
    for migration in sorted(Path(__file__).with_name('migrations').glob('*.sql')):
        version = int(migration.name.split('_')[0])
        if not db.execute('SELECT 1 FROM schema_version WHERE version=?', (version,)).fetchone():
            db.executescript(migration.read_text())
    if not db.execute('SELECT 1 FROM levels').fetchone():
        with db:
            for pos, name in enumerate(['Acogida', 'Formación inicial', 'Formación continua'], 1):
                level = db.execute('INSERT INTO levels(name,position) VALUES (?,?)', (name, pos)).lastrowid
                db.execute('INSERT INTO requirements(level_id,title) VALUES (?,?)',
                           (level, 'Revisión de formación con la catequista'))


def close_db(_=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
