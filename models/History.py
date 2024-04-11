from sqlalchemy import Column, Integer, String, ForeignKey
from models.Video import Video
from models.User import User
from __main__ import Base

class History(Base):
    __tablename__='history'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    video_id = Column(Integer, ForeignKey(Video.id), nullable=False)