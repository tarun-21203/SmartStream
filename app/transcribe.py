from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, VideoUnavailable

def videoID(url):
    id = ''
    for char in url[::-1]:
        if char == '=' : 
            break 
        id += char 
    return id[::-1]

def transcribe_func(videoURL):
    try:
    #     video_id = videoID(videoURL)
    #     print(f"Attempting to fetch transcript for video ID: {video_id}")
    #     transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
    #     text = ' '.join([entry['text'] for entry in transcript])
    #     return {'summary': text}
    # except Exception as e:
    #     print(f"Error fetching transcript: {str(e)}")
    #     return {'Error': str(e)}
        print(f"Received video URL: {videoURL}")
        video_id = videoID(videoURL)
        print(f"Extracted video ID: {video_id}")
            
        print(f"Attempting to fetch transcript for video ID: {video_id}")
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        print(f"Transcript fetched successfully. Number of entries: {len(transcript)}")
            
        text = ' '.join([entry['text'] for entry in transcript])
        print(f"Transcript combined into text. Length of text: {len(text)}")
        return {'summary': text}
    except TranscriptsDisabled:
        error_message = "Transcripts are disabled for this video."
        print(error_message)
        return {'Error': error_message}
    except VideoUnavailable:
        error_message = "The video is unavailable."
        print(error_message)
        return {'Error': error_message}
    except Exception as e:
        error_message = f"Error fetching transcript: {str(e)}"
        print(error_message)
        return {'Error': error_message}