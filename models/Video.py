from sqlalchemy import Column, Integer, String, Text, Float
from sql import Base

class Video(Base):
    __tablename__='video'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    genre = Column(String(50), nullable=False)
    release_year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)