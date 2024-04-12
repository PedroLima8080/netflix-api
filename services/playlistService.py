from models.Playlist import Playlist
from flask_jwt_extended import jwt_required
from flask import jsonify

class PlaylistService:
    session = None
 
    def __init__(self, session):
        self.session = session

    def create_playlist(self, user_id, data):
        if 'name' not in data:
            return jsonify({'error': 'Missing required fields'}), 400

        new_playlist = Playlist(user_id=user_id, name=data['name'])

        self.session.add(new_playlist)
        self.session.commit()

        return jsonify({'message': 'Playlist created successfully'}), 201

    def get_playlists(self, user_id):
        playlists = self.session.query(Playlist).filter_by(user_id=user_id).all()
        serialized_playlists = [{'id': playlist.id, 'user_id': playlist.user_id, 'name': playlist.name} for playlist in playlists]
        return jsonify(serialized_playlists)

    def get_playlist(self, user_id, playlist_id):
        playlist = self.session.query(Playlist).filter_by(id=playlist_id, user_id=user_id).first()
        if not playlist:
            return jsonify({'error': 'Playlist not found'}), 404
        serialized_playlist = {'id': playlist.id, 'user_id': playlist.user_id, 'name': playlist.name}
        return jsonify(serialized_playlist)

    def delete_playlist(self, user_id, playlist_id):
        playlist = self.session.query(Playlist).filter_by(id=playlist_id, user_id=user_id).first()

        if not playlist:
            return jsonify({'error': 'Playlist not found or unauthorized'}), 404

        self.session.delete(playlist)
        self.session.commit()

        return jsonify({'message': 'Playlist deleted successfully'})