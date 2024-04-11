from models.Playlist import Playlist
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify
from __main__ import session

class PlaylistService:
    def create_playlist(self, data):
        if 'name' not in data:
            return jsonify({'error': 'Missing required fields'}), 400

        new_playlist = Playlist(user_id=get_jwt_identity(), name=data['name'])

        session.add(new_playlist)
        session.commit()

        return jsonify({'message': 'Playlist created successfully'}), 201

    def get_playlists(self):
        playlists = session.query(Playlist).filter_by(user_id=get_jwt_identity()).all()
        serialized_playlists = [{'id': playlist.id, 'user_id': playlist.user_id, 'name': playlist.name} for playlist in playlists]
        return jsonify(serialized_playlists)

    def get_playlist(self, playlist_id):
        playlist = session.query(Playlist).filter_by(id=playlist_id, user_id=get_jwt_identity()).first()
        if not playlist:
            return jsonify({'error': 'Playlist not found'}), 404
        serialized_playlist = {'id': playlist.id, 'user_id': playlist.user_id, 'name': playlist.name}
        return jsonify(serialized_playlist)

    def delete_playlist(self, playlist_id):
        playlist = session.query(Playlist).filter_by(id=playlist_id, user_id=get_jwt_identity()).first()

        if not playlist:
            return jsonify({'error': 'Playlist not found or unauthorized'}), 404

        session.delete(playlist)
        session.commit()

        return jsonify({'message': 'Playlist deleted successfully'})