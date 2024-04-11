from models.Video import Video
from models.History import History
from flask import Flask, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from __main__ import session
from services.videoService import VideoService

def init(app):
    videoService = VideoService()
    
    @app.route('/videos', methods=['POST'])
    @jwt_required()
    def create_video():
        return videoService.create_video(request.json)

    @app.route('/videos/<int:video_id>', methods=['PUT'])
    @jwt_required()
    def update_video(video_id):
        return videoService.update_video(request.json, video_id)
    
    @app.route('/videos', methods=['GET'])
    @jwt_required()
    def get_videos():
        return videoService.get_videos()
       
    @app.route('/videos/search', methods=['GET'])
    @jwt_required()
    def search():
        return videoService.search(request.args.get('q'))
        
    @app.route('/videos/<int:video_id>', methods=['GET'])
    @jwt_required()
    def get_video(video_id):
        return videoService.get_video(video_id)

    @app.route('/videos/<int:video_id>/play', methods=['POST'])
    @jwt_required()
    def play_video(video_id):
        return videoService.play_video(video_id)

    @app.route('/videos/<int:video_id>', methods=['DELETE'])
    @jwt_required()
    def delete_video(video_id):
        return videoService.delete_video(video_id)
