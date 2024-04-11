from models.Playlist import Playlist
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Flask, request, jsonify
from __main__ import session
from services.playlistService import PlaylistService

def init(app):
    playlistService = PlaylistService()
    @app.route('/playlist', methods=['POST'])
    @jwt_required()
    def create_playlist():
        return playlistService.create_playlist(request.json)
        
    @app.route('/playlist', methods=['GET'])
    @jwt_required()
    def get_playlists():
        return playlistService.get_playlists()
        
    @app.route('/playlist/<int:playlist_id>', methods=['GET'])
    @jwt_required()
    def get_playlist(playlist_id):
        return playlistService.get_playlist(playlist_id)
        
    @app.route('/playlist/<int:playlist_id>', methods=['DELETE'])
    @jwt_required()
    def delete_playlist(playlist_id):
        return playlistService.delete_playlist(playlist_id)