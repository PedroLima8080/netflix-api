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

@pytest.fixture
def playlist_video_service():
    from services.playlistVideoService import PlaylistVideoService
    return PlaylistVideoService(db['session'])

def create_user_for_test(auth_service):
    response = auth_service.register({'username': 't', 'email': 'p@g.c', 'password': '123'})
    return response[0].json['user_id']

def create_playlist_for_test(auth_service, playlist_service):
        user_id = create_user_for_test(auth_service)
        result = playlist_service.create_playlist(user_id, {'name': 'name...'})
        playlist_id = result[0].json['id']
        return user_id, playlist_id

def test_add_playlist_video(app, auth_service, playlist_service, playlist_video_service):
    with app.app_context():
        user_id, playlist_id = create_playlist_for_test(auth_service, playlist_service)
        result = playlist_video_service.create_playlist_video(user_id, {'video_id': 1}, playlist_id)
        assert result[1] == 201
        result = playlist_video_service.create_playlist_video(user_id, {}, playlist_id)
        assert result[1] == 400

def test_get_playlist_video(app, auth_service, playlist_service, playlist_video_service):
    with app.app_context():
        user_id, playlist_id = create_playlist_for_test(auth_service, playlist_service)
        result = playlist_video_service.get_playlist_videos(user_id, playlist_id)
        assert len(result.json) == 0
        playlist_video_service.create_playlist_video(user_id, {'video_id': 1}, playlist_id)
        result = playlist_video_service.get_playlist_videos(user_id, playlist_id)
        assert len(result.json) == 1

def test_delete_playlist_video(app, auth_service, playlist_service, playlist_video_service):
    with app.app_context():
        user_id, playlist_id = create_playlist_for_test(auth_service, playlist_service)
        playlist_video_service.create_playlist_video(user_id, {'video_id': 1}, playlist_id)
        result = playlist_video_service.get_playlist_videos(user_id, playlist_id)
        assert len(result.json) == 1
        playlist_video_service.delete_playlist_video(user_id, playlist_id, 1)
        result = playlist_video_service.get_playlist_videos(user_id, playlist_id)
        assert len(result.json) == 0
