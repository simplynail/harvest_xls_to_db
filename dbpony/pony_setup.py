import os
from pony import orm

import dbpony.pony_models as models

db_path=r'C:\Users\pawel\OneDrive\Dokumenty\python_Projects\scan_hvac_workbooks\example_data'
db_name='db.sqlite'
db_path = os.path.join(db_path,db_name)

models.db.bind('sqlite', db_path, create_db=True)
orm.sql_debug(False)
models.db.generate_mapping(create_tables=True)