from __main__ import session
from models.User import User
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask import Flask, jsonify

class AuthService:
    def register(self, data):
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        new_user = User(username=username, email=email, password=password)
        session.add(new_user)
        session.commit()
        return jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201

    def login(self, data):
        email = data.get('email')
        password = data.get('password')
        user = session.query(User).filter_by(email=email, password=password).first()
        if user:
            access_token = create_access_token(identity=user.id)
            return jsonify({'message': 'Login successful', 'user_id': user.id, 'access_token': access_token}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401