from flask_jwt_extended import jwt_required, create_access_token
from flask import Flask, jsonify

class AuthService():
    session = None
 
    def __init__(self, session):
        self.session = session
        
    def register(self, data):
        from models.User import User
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        new_user = User(username=username, email=email, password=password)
        self.session.add(new_user)
        self.session.commit()
        return jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201

    def login(self, data):
        from models.User import User
        email = data.get('email')
        password = data.get('password')
        user = self.session.query(User).filter_by(email=email, password=password).first()
        if user:
            access_token = create_access_token(identity=user.id)
            return jsonify({'message': 'Login successful', 'user_id': user.id, 'access_token': access_token}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401