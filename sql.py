import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# Define global variables for engine and session
global_engine = None
global_session = None
Base = None

def init(test=False):
    global global_engine, global_session, Base

    if global_engine is None or global_session is None:
        url = None
        if test:
            url = 'sqlite:///' + os.path.join('database', 'db.sqlite.test')
        else: 
            url = 'sqlite:///' + os.path.join('database', 'db.sqlite')

        engine = create_engine(url)
        session = sessionmaker(bind=engine)
        global_engine = engine
        global_session = session()
        Base = declarative_base()

    return {'engine': global_engine, 'session': global_session, 'base': Base}
