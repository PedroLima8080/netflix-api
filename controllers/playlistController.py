from models.Playlist import Playlist
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Flask, request, jsonify
from services.playlistService import PlaylistService
from __main__ import session

def init(app):
    playlistService = PlaylistService(session)
    @app.route('/playlist', methods=['POST'])
    @jwt_required()
    def create_playlist():
        return playlistService.create_playlist(get_jwt_identity(), request.json)
        
    @app.route('/playlist', methods=['GET'])
    @jwt_required()
    def get_playlists():
        return playlistService.get_playlists(get_jwt_identity())
        
    @app.route('/playlist/<int:playlist_id>', methods=['GET'])
    @jwt_required()
    def get_playlist(playlist_id):
        return playlistService.get_playlist(get_jwt_identity(), playlist_id)
        
    @app.route('/playlist/<int:playlist_id>', methods=['DELETE'])
    @jwt_required()
    def delete_playlist(playlist_id):
        return playlistService.delete_playlist(get_jwt_identity(), playlist_id)