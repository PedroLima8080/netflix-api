from flask import Flask, request, jsonify
import pytest
from sql import init
from flask_jwt_extended import JWTManager

app = None
db = None

def create_user(auth_service):
    data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpassword'}
    return auth_service.register(data)

@pytest.fixture
def auth_service():
    global app, db
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'your_secret_key'
    JWTManager(app)
    
    db = init(True)
    from services.authService import AuthService
    authService = AuthService(db['session'])
    db['base'].metadata.create_all(db['engine'])
    clear_database()
    return authService

@pytest.fixture(autouse=True)
def onFinish():
    clear_database()
        
def clear_database():
    global db
    if db and db['session']:
        db['session'].rollback()
        from models.User import User
        db['session'].query(User).delete()
        db['session'].commit()
    
def test_register(auth_service):
    with app.app_context():
        response = create_user(auth_service)
        assert response[1] == 201
        assert 'user_id' in response[0].json

def test_login(auth_service):
    with app.app_context():
        create_user(auth_service)
        response = auth_service.login({'email': 'test@example.com', 'password': 'testpassword'})

        assert response[1] == 200
        assert 'user_id' in response[0].json
        assert 'access_token' in response[0].json

        response = auth_service.login({'email': 'test@example.com', 'password': 'wrongPassword'})
        assert response[1] == 401
        assert response[0].json['message'] == 'Invalid credentials'

