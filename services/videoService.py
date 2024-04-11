from __main__ import session
from models.Video import Video
from models.History import History
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask import Flask, jsonify

class VideoService:
    def create_video(self, data):
        required_fields = ['title', 'description', 'genre', 'release_year', 'rating']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        new_video = Video(
            title=data['title'],
            description=data['description'],
            genre=data['genre'],
            release_year=data['release_year'],
            rating=data['rating']
        )
        session.add(new_video)
        session.commit()
        return jsonify({'message': 'Video created successfully', 'id': new_video.id}), 201
    
    def update_video(self, data, video_id):
        required_fields = ['title', 'description', 'genre', 'release_year', 'rating']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        video = session.query(Video).get(video_id)
        if not video:
            return jsonify({'error': 'Video not found'}), 404

        video.title = data['title']
        video.description = data['description']
        video.genre = data['genre']
        video.release_year = data['release_year']
        video.rating = data['rating']

        session.commit()

        return jsonify({'message': 'Video updated successfully'})
    
    def get_videos(self):
        videos = session.query(Video).all()
        return jsonify([{'id': v.id, 'title': v.title, 'description': v.description, 'genre': v.genre, 'release_year': v.release_year, 'rating': v.rating} for v in videos]), 200

    def search(query):
        videos = session.query(Video).filter(Video.title.ilike(f"%{query}%")).all()
        return jsonify([{'id': v.id, 'title': v.title, 'description': v.description, 'genre': v.genre, 'release_year': v.release_year, 'rating': v.rating} for v in videos]), 200

    def get_video(self, video_id):
        video = session.query(Video).get(video_id)
        if video:
            return jsonify({'id': video.id, 'title': video.title, 'description': video.description, 'genre': video.genre, 'release_year': video.release_year, 'rating': video.rating}), 200
        else:
            return jsonify({'message': 'Video not found'}), 404

    def play_video(self, video_id):
        new_history = History(user_id=get_jwt_identity(), video_id=video_id)
        session.add(new_history)
        session.commit()
        return jsonify({'message': 'Video playback started'}), 200
    
    def delete_video(self, video_id):
        video = session.query(Video).get(video_id)
        if not video:
            return jsonify({'error': 'Video not found'}), 404

        session.delete(video)
        session.commit()

        return jsonify({'message': 'Video deleted successfully'})