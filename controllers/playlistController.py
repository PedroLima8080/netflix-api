from models.Playlist import Playlist
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Flask, request, jsonify
from __main__ import session

def init(app):
    @app.route('/playlist', methods=['POST'])
    @jwt_required()
    def create_playlist():
        data = request.json
        if 'name' not in data:
            return jsonify({'error': 'Missing required fields'}), 400

        new_playlist = Playlist(user_id=get_jwt_identity(), name=data['name'])

        session.add(new_playlist)
        session.commit()

        return jsonify({'message': 'Playlist created successfully'}), 201

    @app.route('/playlist', methods=['GET'])
    @jwt_required()
    def get_playlists():
        playlists = session.query(Playlist).filter_by(user_id=get_jwt_identity()).all()
        serialized_playlists = [{'id': playlist.id, 'user_id': playlist.user_id, 'name': playlist.name} for playlist in playlists]
        return jsonify(serialized_playlists)

    @app.route('/playlist/<int:playlist_id>', methods=['GET'])
    @jwt_required()
    def get_playlist(playlist_id):
        playlist = session.query(Playlist).filter_by(id=playlist_id, user_id=get_jwt_identity()).first()
        if not playlist:
            return jsonify({'error': 'Playlist not found'}), 404
        serialized_playlist = {'id': playlist.id, 'user_id': playlist.user_id, 'name': playlist.name}
        return jsonify(serialized_playlist)

    @app.route('/playlist/<int:playlist_id>', methods=['DELETE'])
    @jwt_required()
    def delete_playlist(playlist_id):
        playlist = session.query(Playlist).filter_by(id=playlist_id, user_id=get_jwt_identity()).first()

        if not playlist:
            return jsonify({'error': 'Playlist not found or unauthorized'}), 404

        session.delete(playlist)
        session.commit()

        return jsonify({'message': 'Playlist deleted successfully'})