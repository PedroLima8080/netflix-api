from models.History import History
from flask_jwt_extended import jwt_required
from flask import jsonify

class HistoryService:
    session = None
 
    def __init__(self, session):
        self.session = session

    def add_history(self, user_id, video_id):
        new_history = History(user_id=user_id, video_id=video_id)
        self.session.add(new_history)
        self.session.commit()
        return new_history
        
    def get_user_history(self, user_id):  
        user_history = self.session.query(History).filter_by(user_id=user_id).all()
        serialized_history = [{'id': entry.id, 'user_id': entry.user_id, 'video_id': entry.video_id} for entry in user_history]
        return jsonify(serialized_history)
    
    def delete_history_entry(self, user_id, history_id):
        history_entry = self.session.query(History).get(history_id)
        if not history_entry:
            return jsonify({'error': 'History entry not found'}), 404

        if history_entry.user_id != user_id:
            return jsonify({'error': 'Unauthorized access to history entry'}), 403

        self.session.delete(history_entry)
        self.session.commit()
        return jsonify({'message': 'History item deleted'})