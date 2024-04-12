import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = None

def init(test = False):
    url = None
    if test:
        url = 'sqlite:///' + os.path.join('database', 'db.sqlite.test')
    else: 
        url = 'sqlite:///' + os.path.join('database', 'db.sqlite')
    
    engine = create_engine(url)
    session = sessionmaker(bind=engine)
    base = declarative_base()
    global Base
    Base = base
    return {'engine': engine,'session': session(), 'base': base}