from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import sql

app = Flask('__main__')

app.config['JWT_SECRET_KEY'] = 'your_secret_key'

db = sql.init(app)
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
    db.create_all()

app.run(debug=True)