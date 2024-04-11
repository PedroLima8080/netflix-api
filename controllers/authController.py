from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from services.authService import AuthService
from flask import request

def init(app):
    authService = AuthService()
    @app.route('/auth/register', methods=['POST'])
    def register():
        return authService.register(request.json)

    @app.route('/auth/login', methods=['POST'])
    def login():
        return authService.login(request.json)