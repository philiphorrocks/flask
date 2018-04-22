# Quickly query DB using SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect

engine = create_engine('sqlite:///inventory.sqlite', echo=False)

connection = engine.connect()

def getTableNames():

    inspector = inspect(engine)

    # Get table information
    print('Table Name: ' + str(inspector.get_table_names()))

    # Get column information
    print('Column Info: ' + str(inspector.get_columns('groups')))


def dumpData():
# select everythng from the groups table*
    result = engine.execute('SELECT * FROM ''"groups"')
    for _r in result:
       print(_r)

if __name__ == '__main__':
    dumpData()
    getTableNames()
