import requests
import json
from flask import Blueprint, request, jsonify
from . import query 
from youtube_transcript_api import YouTubeTranscriptApi

bp = Blueprint('main', __name__)

@bp.route("/hello", methods=["GET"])
def hello():
    return "hello world"

@bp.route('/transcribe', methods=['POST'])
def transcribe():
    data = request.json
    videoURL = data.get('videoURL')
    if not videoURL:
        return jsonify({'error': "No video URL provided"}), 400
    
    print(f"Received transcription request for URL: {videoURL}")
    response = query.transcribe_and_store(videoURL)
    
    if 'Error' in response:
        print(f"Transcription error: {response['Error']}")
        return jsonify(response), 500
    
    return jsonify(response)


@bp.route('/query',methods=['POST'])
def q():
    data = request.json
    qu = data.get('query')
    prompt = "Answer as if you are answering by analyzing the video only not it's transcribe " + qu
    if not qu : return jsonify({'error' : 'Please enter a query'})
    response = query.query_transcript(prompt)
    return jsonify(response)