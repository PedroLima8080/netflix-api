from models.History import History
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Flask, request, jsonify
from services.historyService import HistoryService
from __main__ import session

def init(app):
    historyService = HistoryService(session)
    @app.route('/history', methods=['GET'])
    @jwt_required()  
    def get_user_history():
        return historyService.get_user_history(get_jwt_identity())
    
    @app.route('/history/<int:history_id>', methods=['DELETE'])
    @jwt_required()  
    def delete_history_entry(history_id):
        return historyService.delete_history_entry(get_jwt_identity(), history_id)