from flask import Flask, request, jsonify
import pytest
from sql import init
from flask_jwt_extended import JWTManager
from app_setup import app_setup

db = init(True)
import models.Models

@pytest.fixture
def app():
    app = app_setup()
    with app.app_context():
        db['base'].metadata.create_all(db['engine'])
        
    yield app

    with app.app_context():
        db['base'].metadata.drop_all(db['engine'])
