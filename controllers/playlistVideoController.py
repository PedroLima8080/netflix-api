from models.PlaylistVideo import PlaylistVideo
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Flask, request, jsonify
from services.playlistVideoService import PlaylistVideoService
from __main__ import session

def init(app):
    playlistVideoService = PlaylistVideoService(session)
    @app.route('/playlist/<int:playlist_id>/videos', methods=['POST'])
    @jwt_required()
    def create_playlist_video(playlist_id):
        return playlistVideoService.create_playlist_video(get_jwt_identity(), request.json, playlist_id)

    @app.route('/playlist/<int:playlist_id>/videos', methods=['GET'])
    @jwt_required()
    def get_playlist_videos(playlist_id):
        return playlistVideoService.get_playlist_videos(get_jwt_identity(), playlist_id)

    @app.route('/playlist/<int:playlist_id>/videos/<int:playlist_video_id>', methods=['DELETE'])
    @jwt_required()
    def delete_playlist_video(playlist_id, playlist_video_id):
        return playlistVideoService.delete_playlist_video(get_jwt_identity(), playlist_id, playlist_video_id)