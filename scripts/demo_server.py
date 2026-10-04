"""Servidor reproducible para grabar la demo, aislado del registro de Noris."""
from pathlib import Path
import argparse
from sendero import create_app
from sendero.db import get_db
from sendero.services import save_child, record_attendance, today

parser=argparse.ArgumentParser(description='Demo ficticia aislada de Sendero')
parser.add_argument('--database',default='artifacts/demo.sqlite')
parser.add_argument('--empty',action='store_true',help='Iniciar sin crear fichas ficticias')
parser.add_argument('--test-code',action='store_true',help='Usar demo-ficticia como acceso de esta demo aislada')
parser.add_argument('--port',type=int,default=5082)
args=parser.parse_args()
database=Path(args.database).resolve()
database.parent.mkdir(parents=True,exist_ok=True)
config={'DATABASE':str(database)}
if args.test_code:
    config.update(ACCESS_CODE='demo-ficticia',SECRET_KEY='solo-demo-ficticia-no-produccion')
app=create_app(config)
with app.app_context():
    if not args.empty and not get_db().execute('SELECT 1 FROM children').fetchone():
        for name,level in [('Lucía Ejemplo',1),('Mateo Ejemplo',1),('Sofía Ejemplo',2)]:
            c=save_child({'name':name,'guardian':'Responsable ficticio','contact':'','joined':today(),'level_id':level})
            record_attendance(c['id'],{'day':today(),'topic':'Encuentro de formación · ejemplo','present':True})
app.run(host='127.0.0.1',port=args.port,debug=False)
