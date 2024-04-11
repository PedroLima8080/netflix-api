from models.Video import Video
from models.History import History
from flask import Flask, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from __main__ import db

def init(app):
    @app.route('/videos', methods=['POST'])
    @jwt_required()
    def create_video():
        data = request.json
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
        db.session.add(new_video)
        db.session.commit()
        return jsonify({'message': 'Video created successfully', 'id': new_video.id}), 201
    
    @app.route('/videos/<int:video_id>', methods=['PUT'])
    @jwt_required()
    def update_video(video_id):
        data = request.json

        required_fields = ['title', 'description', 'genre', 'release_year', 'rating']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        video = Video.query.get(video_id)
        if not video:
            return jsonify({'error': 'Video not found'}), 404

        video.title = data['title']
        video.description = data['description']
        video.genre = data['genre']
        video.release_year = data['release_year']
        video.rating = data['rating']

        db.session.commit()

        return jsonify({'message': 'Video updated successfully'})
    
    @app.route('/videos', methods=['GET'])
    @jwt_required()
    def get_videos():
        videos = Video.query.all()
        return jsonify([{'id': v.id, 'title': v.title, 'description': v.description, 'genre': v.genre, 'release_year': v.release_year, 'rating': v.rating} for v in videos]), 200

    @app.route('/videos/search', methods=['GET'])
    @jwt_required()
    def search():
        query = request.args.get('q')
        videos = Video.query.filter(Video.title.ilike(f"%{query}%")).all()
        return jsonify([{'id': v.id, 'title': v.title, 'description': v.description, 'genre': v.genre, 'release_year': v.release_year, 'rating': v.rating} for v in videos]), 200


    @app.route('/videos/<int:video_id>', methods=['GET'])
    @jwt_required()
    def get_video(video_id):
        video = Video.query.get(video_id)
        if video:
            return jsonify({'id': video.id, 'title': video.title, 'description': video.description, 'genre': video.genre, 'release_year': video.release_year, 'rating': video.rating}), 200
        else:
            return jsonify({'message': 'Video not found'}), 404

    @app.route('/videos/<int:video_id>/play', methods=['POST'])
    @jwt_required()
    def play_video(video_id):
        new_history = History(user_id=get_jwt_identity(), video_id=video_id)
        db.session.add(new_history)
        db.session.commit()
        return jsonify({'message': 'Video playback started'}), 200
    
    @app.route('/videos/<int:video_id>', methods=['DELETE'])
    @jwt_required()
    def delete_video(video_id):
        video = Video.query.get(video_id)
        if not video:
            return jsonify({'error': 'Video not found'}), 404

        db.session.delete(video)
        db.session.commit()

        return jsonify({'message': 'Video deleted successfully'})