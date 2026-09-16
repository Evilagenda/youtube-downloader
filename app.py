import os
from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

COOKIE_FILE_PATH = "cookies.txt"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/info', methods=['POST'])
def get_info():
    data = request.get_json() or {}
    url = data.get('url', '').strip()

    if not url:
        return jsonify({'error': 'Please provide a valid URL'}), 400

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['mweb', 'web', 'ios']
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    }

    if os.path.exists(COOKIE_FILE_PATH):
        ydl_opts['cookiefile'] = COOKIE_FILE_PATH

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            raw_formats = info.get('formats', [])
            extracted_formats = []
            seen_resolutions = set()

            for f in reversed(raw_formats):
                download_url = f.get('url')
                if not download_url:
                    continue

                res = f.get('format_note') or f.get('resolution') or 'Unknown'
                ext = f.get('ext', 'mp4')

                if res not in seen_resolutions:
                    seen_resolutions.add(res)
                    extracted_formats.append({
                        'resolution': res,
                        'ext': ext,
                        'url': download_url
                    })

            return jsonify({
                'title': info.get('title', 'Video'),
                'thumbnail': info.get('thumbnail', ''),
                'duration': info.get('duration', 0),
                'formats': extracted_formats
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
