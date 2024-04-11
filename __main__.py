from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from sqlalchemy.orm import declarative_base

import sql

app = Flask('__main__')

app.config['JWT_SECRET_KEY'] = 'your_secret_key'

result = sql.init(app)
engine = result['engine']
session = result['session']
Base = declarative_base()
jwt = JWTManager(app)

from models.History import History
from models.Playlist import Playlist
from models.PlaylistVideo import PlaylistVideo
from models.Video import Video
from models.User import User

import controllers.videoController
import controllers.authController
import controllers.playlistController
import controllers.playlistVideoController
import controllers.historyController
controllers.videoController.init(app)
controllers.authController.init(app)
controllers.playlistController.init(app)
controllers.playlistVideoController.init(app)
controllers.historyController.init(app)

with app.app_context():
    Base.metadata.create_all(engine)

app.run(debug=True)