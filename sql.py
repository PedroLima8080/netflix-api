from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

def init(app):
    # url = URL.create(
    # drivername="postgresql",
    # username="coderpad",
    # host="/tmp/postgresql/socket",
    # database="coderpad"
    # )
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # return SQLAlchemy(app)
    engine = create_engine('sqlite:///db.sqlite')
    Session = sessionmaker(bind=engine)
    return {'engine': engine,'session': Session()}