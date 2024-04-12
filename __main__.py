from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from sqlalchemy.orm import declarative_base
from app_setup import app_setup

import sql

app = app_setup()
result = sql.init()
engine = result['engine']
session = result['session']
Base = result['base']

import models.Models

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