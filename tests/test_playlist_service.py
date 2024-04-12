import pytest
from app_setup import app_setup
from sql import init
from sqlalchemy import MetaData

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
def playlist_service():
    from services.playlistService import PlaylistService
    return PlaylistService(db['session'])

def create_user_for_test(auth_service):
    response = auth_service.register({'username': 't', 'email': 'p@g.c', 'password': '123'})
    return response[0].json['user_id']

def test_add_playlist(app, auth_service, playlist_service):
    with app.app_context():
        user_id = create_user_for_test(auth_service)
        result = playlist_service.get_playlists(user_id)
        assert len(result.json) == 0
        playlist_service.create_playlist(user_id, {'name': 'name...'})
        result = playlist_service.get_playlists(user_id)
        assert len(result.json) == 1