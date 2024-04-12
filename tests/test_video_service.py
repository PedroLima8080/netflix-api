import pytest
from app_setup import app_setup
from sql import init

def create_user_for_test(auth_service):
    auth_service.register({'username': 't', 'email': 'p@g.c', 'password': '123'})

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
    assert True
    # from services.authService import AuthService
    # db = init(True)
    # return AuthService(db['session'])

@pytest.fixture
def video_service():
    from services.videoService import VideoService
    db = init(True)
    return VideoService(db['session'])

def test_add_video(app, video_service):
    with app.app_context():
        response = video_service.create_video({
            'title': 'title',
            'description': 'description',
            'genre': 'genre',
            'release_year': 'release_year',
            'rating': 5,
        })
        assert response[1] == 201
        response = video_service.create_video({
            'title': 'title',
            'genre': 'genre',
            'release_year': 'release_year',
            'rating': 'rating',
        })
        assert response[1] == 400
