from sqlalchemy import Column, Integer, String, ForeignKey
from sql import Base
from models.User import User

class Playlist(Base):
    __tablename__='playlist'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    name = Column(String(100), nullable=False)