"""Servidor reproducible para grabar la demo, aislado del registro de Noris."""
from pathlib import Path
import argparse
from sendero import create_app
from sendero.db import get_db
from sendero.services import save_child, record_attendance, today

parser=argparse.ArgumentParser(description='Demo ficticia aislada de Sendero')
parser.add_argument('--database',default='artifacts/demo.sqlite')
parser.add_argument('--port',type=int,default=5082)
args=parser.parse_args()
database=Path(args.database).resolve()
database.parent.mkdir(exist_ok=True)
app=create_app({'DATABASE':str(database)})
with app.app_context():
    if not get_db().execute('SELECT 1 FROM children').fetchone():
        for name,level in [('Lucía Ejemplo',1),('Mateo Ejemplo',1),('Sofía Ejemplo',2)]:
            c=save_child({'name':name,'guardian':'Responsable ficticio','contact':'','joined':today(),'level_id':level})
            record_attendance(c['id'],{'day':today(),'topic':'Encuentro de formación · ejemplo','present':True})
app.run(host='127.0.0.1',port=args.port,debug=False)
