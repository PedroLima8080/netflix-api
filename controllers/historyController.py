from models.History import History
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Flask, request, jsonify
from __main__ import session
from services.historyService import HistoryService

def init(app):
    historyService = HistoryService()
    @app.route('/history', methods=['GET'])
    @jwt_required()  
    def get_user_history():
        return historyService.get_user_history()
    
    @app.route('/history/<int:history_id>', methods=['DELETE'])
    @jwt_required()  
    def delete_history_entry(history_id):
        return historyService.delete_history_entry(history_id)