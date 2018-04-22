# Quickly query DB using SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declarative_base

# Create DB engine conenction
engine = create_engine('sqlite:///inventory.sqlite', echo=False)

# Create a metadata object (DB schema object)
metadata = MetaData(engine, reflect=True)

# Use inspector class and create object
inspector = inspect(engine)

# create session
Session = sessionmaker(bind=engine)
session = Session()



def getDBInfo():

    try:

        # Get table information
        for table_name in inspector.get_table_names():
            print("Table name: " + str(table_name))

            # Get column information
            for column_name in inspector.get_columns(table_name):
                 i = 0

                 print("Column: ")
                 print(column_name)

    except:
        print("Error: Could not retrive DB schema")


def dumpData():

    try:

        for table_name in inspector.get_table_names():

             # Auo load data from table
            table = Table(table_name, metadata, autoload=True)

            # select everythng from the groups table
            dataDump = session.query(table).all()

            for _r in dataDump:
                print(_r)

        session.close()

    except:
        print("Error: Cannot get data dump")



if __name__ == '__main__':
    dumpData()
    getDBInfo()
