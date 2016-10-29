from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

Session = sessionmaker()

class Database:
    def __init__(self):
        dbname = os.getenv('PSQL_DB_NAME')
        host = os.getenv('PSQL_DB_HOST')
        port = os.getenv('PSQL_DB_PORT')
        user = os.getenv('PSQL_DB_USER')
        password = os.getenv('PSQL_DB_PASSWORD')

        uri = 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, dbname)
        eng = create_engine(uri)
        Session.configure(bind=eng)
        self.session = Session()
        self.session.commit()

db = Database()
Base = declarative_base()