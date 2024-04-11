from models.PlaylistVideo import PlaylistVideo
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Flask, request, jsonify
from __main__ import db

def init(app):
    @app.route('/playlist/<int:playlist_id>/videos', methods=['POST'])
    @jwt_required()
    def create_playlist_video(playlist_id):
        current_user_id = get_jwt_identity()
        data = request.json

        if 'video_id' not in data:
            return jsonify({'error': 'Missing required fields: playlist_id, video_id'}), 400

        if not is_playlist_owner(current_user_id, playlist_id):
            return jsonify({'error': 'Unauthorized access to playlist'}), 403

        new_playlist_video = PlaylistVideo(playlist_id=playlist_id, video_id=data['video_id'])
        db.session.add(new_playlist_video)
        db.session.commit()

        return jsonify({'message': 'Playlist video created successfully'}), 201

    @app.route('/playlist/<int:playlist_id>/videos', methods=['GET'])
    @jwt_required()
    def get_playlist_videos(playlist_id):
        current_user_id = get_jwt_identity()

        if not is_playlist_owner(current_user_id, playlist_id):
            return jsonify({'error': 'Unauthorized access to playlist'}), 403

        playlist_videos = PlaylistVideo.query.filter_by(playlist_id=playlist_id).all()
        serialized_playlist_videos = [{'id': pv.id, 'playlist_id': pv.playlist_id, 'video_id': pv.video_id} for pv in playlist_videos]
        return jsonify(serialized_playlist_videos)

    @app.route('/playlist/<int:playlist_id>/videos/<int:playlist_video_id>', methods=['DELETE'])
    @jwt_required()
    def delete_playlist_video(playlist_id, playlist_video_id):
        current_user_id = get_jwt_identity()

        playlist_video = PlaylistVideo.query.get(playlist_video_id)
        if not playlist_video:
            return jsonify({'error': 'Playlist video not found'}), 404

        if playlist_video.playlist_id != playlist_id:
            return jsonify({'error': 'Playlist video not associated with provided playlist_id'}), 400

        if not is_playlist_owner(current_user_id, playlist_id):
            return jsonify({'error': 'Unauthorized access to playlist'}), 403

        db.session.delete(playlist_video)
        db.session.commit()

        return jsonify({'message': 'Playlist video deleted successfully'})

    def is_playlist_owner(user_id, playlist_id):
        from models.Playlist import Playlist
        playlist = Playlist.query.filter_by(id=playlist_id, user_id=user_id).first()
        return playlist is not None