from flask import Flask, request, jsonify
import pytest
from sql import init
from flask_jwt_extended import JWTManager
from app_setup import app_setup

@pytest.fixture
def app():
    app = app_setup()
    db = init(True)
    import models.Models
    with app.app_context():
        db['base'].metadata.drop_all(db['engine'])
        db['base'].metadata.create_all(db['engine'])
        
    yield app

    db['base'].metadata.drop_all(db['engine'])
    db['base'].metadata.create_all(db['engine'])

@pytest.fixture
def auth_service():
    from services.authService import AuthService
    db = init(True)
    return AuthService(db['session'])

@pytest.fixture
def user_data():
    return {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpassword'}

def test_register(app, auth_service, user_data):
    with app.app_context():
        response = auth_service.register(user_data)
        assert response[1] == 201
        assert 'user_id' in response[0].json

def test_login(app, auth_service, user_data):
    with app.app_context():
        auth_service.register(user_data)
        response = auth_service.login(user_data)
        assert response[1] == 200
        assert 'user_id' in response[0].json
        assert 'access_token' in response[0].json

        data = user_data
        data['password'] = 'wrongPassword'
        response = auth_service.login(data)
        assert response[1] == 401
        assert response[0].json['message'] == 'Invalid credentials'

