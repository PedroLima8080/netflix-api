from models.History import History
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Flask, request, jsonify
from __main__ import db


def init(app):
    @app.route('/history', methods=['GET'])
    @jwt_required()  
    def get_user_history():
        current_user_id = get_jwt_identity()  

        user_history = History.query.filter_by(user_id=current_user_id).all()
        serialized_history = [{'id': entry.id, 'user_id': entry.user_id, 'video_id': entry.video_id} for entry in user_history]
        return jsonify(serialized_history)
    
    @app.route('/history/<int:history_id>', methods=['DELETE'])
    @jwt_required()  
    def delete_history_entry(history_id):
        current_user_id = get_jwt_identity()  
        
        history_entry = History.query.get(history_id)
        if not history_entry:
            return jsonify({'error': 'History entry not found'}), 404

        if history_entry.user_id != current_user_id:
            return jsonify({'error': 'Unauthorized access to history entry'}), 403

        db.session.delete(history_entry)
        db.session.commit()
        return jsonify({'message': 'History item deleted'})