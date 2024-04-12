from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager

def app_setup():
    app = Flask('__main__')
    app.config['JWT_SECRET_KEY'] = '123'
    jwt = JWTManager(app)

    return app