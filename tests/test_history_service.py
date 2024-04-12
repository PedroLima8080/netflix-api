import pytest
from app_setup import app_setup
from sql import init

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

@pytest.fixture
def auth_service(app):
    from services.authService import AuthService
    return AuthService(db['session'])

@pytest.fixture
def video_service():
    from services.videoService import VideoService
    return VideoService(db['session'])

@pytest.fixture
def history_service():
    from services.historyService import HistoryService
    return HistoryService(db['session'])

@pytest.fixture
def video_data():
    return {
            'title': 'title',
            'description': 'description',
            'genre': 'genre',
            'release_year': 'release_year',
            'rating': 5,
        }


def create_user_for_test(auth_service):
    response = auth_service.register({'username': 't', 'email': 'p@g.c', 'password': '123'})
    return response[0].json['user_id']

def test_play_video_generate_history(app, auth_service, video_service, history_service, video_data):
    with app.app_context():
        user_id = create_user_for_test(auth_service)
        video_id = video_service.create_video(video_data)[0].json['id']
        historic = history_service.get_user_history(user_id).json
        assert len(historic) == 0
        video_service.play_video(user_id, video_id)
        historic = history_service.get_user_history(user_id).json
        assert len(historic) == 1
