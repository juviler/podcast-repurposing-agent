# === Imports ===
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from utils.file_utils import extract_text_from_file
import openai
import os
import re
import tiktoken
import traceback

# === Config ===
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Enable CORS for frontend requests
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# === Routes ===

# Upload and extract transcript from file
@app.route('/transcript', methods=['POST'])
def get_transcript():
    if 'file' in request.files:
        file = request.files['file']
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            transcript = extract_text_from_file(filepath)
            return jsonify({'transcript': transcript})
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    return jsonify({'error': 'No valid input provided'}), 400

# Fetch and return transcript from YouTube URL
@app.route('/transcript-from-youtube', methods=['POST'])
def transcript_from_youtube():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'Missing or invalid JSON body'}), 400

    url = data['url']
    try:
        video_id = extract_video_id(url)
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([entry["text"] for entry in transcript_list])

        # Debug logging
        print("Transcript List:", transcript_list)
        print("Formatted Transcript:", transcript_text)

        return jsonify({'transcript': transcript_text})
    except Exception as e:
        print("Error while getting YouTube transcript:", str(e))
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# Generate repurposed content from transcript
@app.route('/generate-content', methods=['POST'])
def generate_content():
    data = request.get_json()
    transcript = data.get('transcript')
    task_type = data.get('task_type')

    if not transcript or not task_type:
        return jsonify({'error': 'Missing transcript or task_type'}), 400

    try:
        # === Truncate transcript if too long ===
        encoding = tiktoken.encoding_for_model("gpt-4")
        total_input = "You are a helpful assistant. Analyze the following transcript:\n\n" + transcript
        tokens = encoding.encode(total_input)

        max_token_limit = 7500
        warning = None
        if len(tokens) > max_token_limit:
            truncated_tokens = tokens[:max_token_limit]
            transcript = encoding.decode(truncated_tokens)
            percent_used = round(max_token_limit / len(tokens) * 100)
            warning = f"Transcript was too long. Only the first {percent_used}% was included."

        # === Prompt Templates ===
        prompt_templates = {
            'blog_outline': f"""You are a blog strategist. Given the following transcript, extract the core ideas and structure them into a clear blog post outline with 4–6 sections. Be concise and insightful.\n\nTranscript:\n{transcript}""",
            'newsletter_blurb': f"""You are a marketing writer. Summarize the transcript into a short blurb for a newsletter (max 3 sentences). Highlight the most interesting insight and write in an engaging tone.\n\nTranscript:\n{transcript}""",
            'shorts_script': f"""You are a content creator writing a YouTube Shorts script. Using the transcript, write a punchy, engaging script (80–100 words max) that hooks viewers immediately and ends with a CTA to listen to the full episode.\n\nTranscript:\n{transcript}""",
            'quote_finder': f"""You are a quote extractor. From the transcript, identify 3 direct quotes (under 30 words each) that are insightful or provocative. Return only the quotes, no explanation.\n\nTranscript:\n{transcript}""",
            'linkedin_post': f"""You are a social media strategist. Write a LinkedIn post draft that summarizes a key idea from the transcript in a personal, thought-provoking tone. Make it feel authentic and designed to spark conversation.\n\nTranscript:\n{transcript}""",
            'internal_summary': f"""You are an internal communications assistant. Summarize this transcript into a short internal summary (max 5 bullet points) for a team that didn't attend the conversation.\n\nTranscript:\n{transcript}"""
        }

        prompt = prompt_templates.get(task_type)
        if not prompt:
            return jsonify({'error': 'Invalid task_type'}), 400

        # === Generate response via OpenAI ===
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        result = response.choices[0].message.content.strip()
        return jsonify({'result': result, 'warning': warning} if warning else {'result': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Extracts YouTube video ID from full URL
def extract_video_id(url):
    match = re.search(r'(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})', url)
    if not match:
        raise ValueError('Invalid YouTube URL')
    return match.group(1)

# === Launch App ===
if __name__ == '__main__':
    app.run(debug=True)