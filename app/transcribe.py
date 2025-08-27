import os
import re
import time

def extract_video_id(url):
    """Extract video ID from various YouTube URL formats"""
    if not url:
        return None
    
    url = url.strip()
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/v\/([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/watch\?.*v=([a-zA-Z0-9_-]{11})',
        r'youtu\.be\/([a-zA-Z0-9_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    # Fallback method
    if '=' in url:
        fallback_id = url.split('=')[-1].split('&')[0].split('#')[0]
        if len(fallback_id) == 11 and re.match(r'^[a-zA-Z0-9_-]+$', fallback_id):
            return fallback_id
    
    return None

def extract_transcript_yt_dlp(video_url):
    """Extract transcript using yt-dlp"""
    try:
        from yt_dlp import YoutubeDL

        sub_file = f'transcript_{int(time.time())}.en.vtt'

        # yt-dlp options with anti-bot measures
        ydl_opts = {
            'writeautomaticsub': True,
            'writesubtitles': True,
            'subtitleslangs': ['en', 'en-US', 'en-GB', 'en-CA'],
            'subtitlesformat': 'vtt',
            'skip_download': True,
            'outtmpl': sub_file.replace('.en.vtt', '.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            # Anti-bot measures
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                    'player_skip': ['webpage', 'configs'],
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            }
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # Find all .vtt files created by yt-dlp
        import glob
        all_vtt_files = glob.glob('*.vtt')

        final_text = None

        # Process all found .vtt files
        for file_path in all_vtt_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Clean VTT content
                    lines = content.split('\n')
                    clean_text = []
                    for line in lines:
                        line = line.strip()
                        if (not line or line.startswith('WEBVTT') or
                            line.startswith('Kind:') or line.startswith('Language:') or
                            '-->' in line or line.isdigit() or
                            line.startswith('NOTE') or line.startswith('STYLE')):
                            continue

                        # Remove timing codes like <00:00:01.140><c> and </c>
                        import re
                        line = re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}><c>', '', line)
                        line = re.sub(r'</c>', '', line)
                        line = re.sub(r'<[^>]+>', '', line)

                        if line.strip():
                            clean_text.append(line.strip())

                    if clean_text:
                        text = ' '.join(clean_text)

                        # Remove duplicate phrases that sometimes occur
                        words = text.split()
                        cleaned_words = []
                        i = 0
                        while i < len(words):
                            cleaned_words.append(words[i])
                            # Skip duplicate sequences
                            if i + 1 < len(words) and words[i] == words[i + 1]:
                                while i + 1 < len(words) and words[i] == words[i + 1]:
                                    i += 1
                            i += 1

                        final_text = ' '.join(cleaned_words)
                        if final_text.strip():
                            break  # Found good content, stop processing other files

                except Exception:
                    continue

        # Clean up ALL .vtt files immediately after processing
        for vtt_file in all_vtt_files:
            try:
                os.remove(vtt_file)
            except:
                pass

        # Return the processed text if found
        if final_text and final_text.strip():
            return {'success': True, 'text': final_text}

        return {'success': False, 'error': 'No subtitle files found or empty content'}

    except ImportError:
        # Clean up any .vtt files on error
        try:
            import glob
            for vtt_file in glob.glob('*.vtt'):
                try:
                    os.remove(vtt_file)
                except:
                    pass
        except:
            pass
        return {'success': False, 'error': 'yt-dlp not installed'}
    except Exception as e:
        # Clean up any .vtt files on error
        try:
            import glob
            for vtt_file in glob.glob('*.vtt'):
                try:
                    os.remove(vtt_file)
                except:
                    pass
        except:
            pass
        return {'success': False, 'error': str(e)}

def transcribe_func(videoURL):
    """Extract transcript from YouTube video using yt-dlp"""
    try:
        # Extract video ID
        video_id = extract_video_id(videoURL)
        if not video_id:
            return {'Error': 'Could not extract video ID from URL. Please check the YouTube URL format.'}
        
        if len(video_id) != 11:
            return {'Error': 'Invalid video ID format. YouTube video IDs should be 11 characters long.'}
        
        # Extract transcript using yt-dlp
        result = extract_transcript_yt_dlp(videoURL)
        if result['success']:
            return {'summary': result['text']}

        # Extraction failed
        return {'Error': 'No transcripts could be retrieved for this video. The video may not have captions available, may be restricted, or captions may be disabled.'}
        
    except Exception as e:
        return {'Error': f'Unexpected error: {str(e)}'}