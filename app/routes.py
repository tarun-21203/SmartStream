from flask import Blueprint, request, jsonify
from . import query

bp = Blueprint('main', __name__)

@bp.route('/transcribe', methods=['POST'])
def transcribe():
    data = request.json
    videoURL = data.get('videoURL')
    if not videoURL:
        return jsonify({'error': "No video URL provided"}), 400

    response = query.transcribe_and_store(videoURL)

    if 'Error' in response:
        return jsonify({'error': response['Error']}), 500

    return jsonify(response)

@bp.route('/query', methods=['POST'])
def query_video():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        user_query = data.get('query')
        if not user_query:
            return jsonify({'error': 'No query provided'}), 400

        response = query.query_transcript(user_query)

        if 'error' in response:
            return jsonify(response), 500

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500