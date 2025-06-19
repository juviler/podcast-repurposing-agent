import re
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable

def extract_video_id(youtube_url):
    """
    Extracts the 11-character YouTube video ID from a URL.
    
    Accepts both full and shortened formats:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    """
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11})"
    match = re.search(pattern, youtube_url)
    if match:
        return match.group(1)
    raise ValueError("Invalid YouTube URL")

def get_transcript_from_url(youtube_url):
    """
    Retrieves transcript text from a YouTube URL.
    Returns a single string with all transcript text concatenated.
    Raises appropriate exceptions if transcript is unavailable.
    """
    video_id = extract_video_id(youtube_url)

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([entry['text'] for entry in transcript])
        return full_text
    except TranscriptsDisabled:
        raise RuntimeError("Transcripts are disabled for this video.")
    except NoTranscriptFound:
        raise RuntimeError("No transcript found for this video.")
    except VideoUnavailable:
        raise RuntimeError("The video is unavailable.")
    except Exception as e:
        raise RuntimeError(f"Unexpected error while fetching transcript: {e}")
