from models.History import History
from __main__ import session
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify

class HistoryService:
    def get_user_history(self):
        current_user_id = get_jwt_identity()  

        user_history = session.query(History).filter_by(user_id=current_user_id).all()
        serialized_history = [{'id': entry.id, 'user_id': entry.user_id, 'video_id': entry.video_id} for entry in user_history]
        return jsonify(serialized_history)
    
    def delete_history_entry(self, history_id):
        current_user_id = get_jwt_identity()  
        
        history_entry = session.query(History).get(history_id)
        if not history_entry:
            return jsonify({'error': 'History entry not found'}), 404

        if history_entry.user_id != current_user_id:
            return jsonify({'error': 'Unauthorized access to history entry'}), 403

        session.delete(history_entry)
        session.commit()
        return jsonify({'message': 'History item deleted'})