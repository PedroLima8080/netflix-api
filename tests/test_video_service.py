import pytest
from app_setup import app_setup
from sql import init

db = init(True)
import models.Models

def create_user_for_test(auth_service):
    auth_service.register({'username': 't', 'email': 'p@g.c', 'password': '123'})

@pytest.fixture
def app():
    app = app_setup()
    with app.app_context():
        db['base'].metadata.create_all(db['engine'])
        
    yield app

    with app.app_context():
        db['base'].metadata.drop_all(db['engine'])

@pytest.fixture
def auth_service(app):
    from services.authService import AuthService
    return AuthService(db['session'])

@pytest.fixture
def video_service():
    from services.videoService import VideoService
    return VideoService(db['session'])

@pytest.fixture
def video_data():
    return {
            'title': 'title',
            'description': 'description',
            'genre': 'genre',
            'release_year': 'release_year',
            'rating': 5,
        }

def test_add_video(app, video_service, video_data):
    with app.app_context():
        response = video_service.create_video(video_data)
        assert response[1] == 201
        del video_data['description']
        response = video_service.create_video(video_data)
        assert response[1] == 400

def test_list_videos(app, video_service, video_data):
    with app.app_context():
        response = video_service.delete_all()
        response = video_service.get_videos()
        assert len(response[0].json) == 0
        video_service.create_video(video_data)
        response = video_service.get_videos()
        assert len(response[0].json) == 1

def test_update_video(app, video_service, video_data):
    with app.app_context():
        response = video_service.create_video(video_data)
        assert video_data['description'] == 'description'
        video_data['description'] = 'new description'
        video_service.update_video(video_data, 1)
        result = video_service.get_video(1)
        assert result[0].json['description'] == 'new description'

def test_delete_video(app, video_service, video_data):
    with app.app_context():
        response = video_service.create_video(video_data)
        result = video_service.get_video(1)
        assert result[0].json['id'] == 1
        video_service.delete_video(1)
        result = video_service.get_video(1)
        assert result[1] == 404

