from sqlalchemy import Column, Integer, String, ForeignKey
from models.Playlist import Playlist
from models.Video import Video
from sql import Base

class PlaylistVideo(Base):
    __tablename__='playlist_video'
    id = Column(Integer, primary_key=True)
    playlist_id = Column(Integer, ForeignKey(Playlist.id), nullable=False)
    video_id = Column(Integer, ForeignKey(Video.id), nullable=False)