from flask_jwt_extended import jwt_required, create_access_token
from services.authService import AuthService
from flask import request
from __main__ import session

def init(app):
    authService = AuthService(session)
    @app.route('/auth/register', methods=['POST'])
    def register():
        return authService.register(request.json)

    @app.route('/auth/login', methods=['POST'])
    def login():
        return authService.login(request.json)