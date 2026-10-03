import argparse
from . import create_app
from .services import save_child, today
from .db import get_db

parser = argparse.ArgumentParser(description='Sendero · Registro local de catequesis')
parser.add_argument('--demo', action='store_true', help='Añadir tres fichas ficticias a una base vacía')
parser.add_argument('--port', type=int, default=5081)
args = parser.parse_args()
app = create_app()
if args.demo:
    with app.app_context():
        if not get_db().execute('SELECT 1 FROM children').fetchone():
            for name, level in [('Lucía Ejemplo', 1), ('Mateo Ejemplo', 1), ('Sofía Ejemplo', 2)]:
                save_child({'name': name, 'guardian': 'Responsable ficticio', 'contact': '', 'joined': today(), 'level_id': level})
print(f'Sendero: http://127.0.0.1:{args.port}')
print(f'El código privado de acceso está en: {app.instance_path}/access-code')
app.run(host='127.0.0.1', port=args.port, debug=False)
