from models.User import User
from flask import Flask, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from __main__ import db

def init(app):
    @app.route('/auth/register', methods=['POST'])
    def register():
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201

    @app.route('/auth/login', methods=['POST'])
    def login():
        data = request.json
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            access_token = create_access_token(identity=user.id)
            return jsonify({'message': 'Login successful', 'user_id': user.id, 'access_token': access_token}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401