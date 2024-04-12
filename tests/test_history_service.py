import pytest
from sql import init

def create_user_for_test():
    auth_service = auth_service()
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
    from services.authService import AuthService
    db = init(True)
    return AuthService(db['session'])

@pytest.fixture
def history_service():
    from services.historyService import HistoryService
    db = init(True)
    return HistoryService(db['session'])

def test_add_history(history_service):
    assert True

def test_get_user_history(history_service):
    assert True

def test_delete_history_entry(history_service):
    assert True
