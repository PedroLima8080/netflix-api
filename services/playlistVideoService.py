from models.PlaylistVideo import PlaylistVideo
from flask_jwt_extended import jwt_required
from flask import jsonify

class PlaylistVideoService:
    session = None
 
    def __init__(self, session):
        self.session = session

    def create_playlist_video(self, user_id, data, playlist_id):
        if 'video_id' not in data:
            return jsonify({'error': 'Missing required fields: playlist_id, video_id'}), 400

        if not self.is_playlist_owner(user_id, playlist_id):
            return jsonify({'error': 'Unauthorized access to playlist'}), 403

        new_playlist_video = PlaylistVideo(playlist_id=playlist_id, video_id=data['video_id'])
        self.session.add(new_playlist_video)
        self.session.commit()

        return jsonify({'message': 'Playlist video created successfully'}), 201

    def get_playlist_videos(self, user_id, playlist_id):
        if not self.is_playlist_owner(user_id, playlist_id):
            return jsonify({'error': 'Unauthorized access to playlist'}), 403

        playlist_videos = self.session.query(PlaylistVideo).filter_by(playlist_id=playlist_id).all()
        serialized_playlist_videos = [{'id': pv.id, 'playlist_id': pv.playlist_id, 'video_id': pv.video_id} for pv in playlist_videos]
        return jsonify(serialized_playlist_videos)

    def delete_playlist_video(self, user_id, playlist_id, playlist_video_id):
        playlist_video = self.session.get(PlaylistVideo, playlist_video_id)
        if not playlist_video:
            return jsonify({'error': 'Playlist video not found'}), 404

        if playlist_video.playlist_id != playlist_id:
            return jsonify({'error': 'Playlist video not associated with provided playlist_id'}), 400

        if not self.is_playlist_owner(user_id, playlist_id):
            return jsonify({'error': 'Unauthorized access to playlist'}), 403

        self.session.delete(playlist_video)
        self.session.commit()

        return jsonify({'message': 'Playlist video deleted successfully'})

    def is_playlist_owner(self, user_id, playlist_id):
        from models.Playlist import Playlist
        playlist = self.session.query(Playlist).filter_by(id=playlist_id, user_id=user_id).first()
        return playlist is not None