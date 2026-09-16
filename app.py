from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return "YouTube Downloader API is Live!"

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    video_url = data.get('url') if data else None
    format_type = data.get('format_type', 'video') if data else 'video'

    if not video_url:
        return jsonify({'error': 'Please provide a valid YouTube URL'}), 400

    format_selector = 'bestaudio/best' if format_type == 'audio' else 'best/bestvideo+bestaudio'

    ydl_opts = {
        'format': format_selector,
        'quiet': True,
        'no_warnings': True,
        'cookiefile': 'cookies.txt',
        'extractor_args': {
            'youtube': {
                'player_client': ['mweb', 'ios']
            }
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            download_url = info.get('url')

            if not download_url and 'requested_formats' in info:
                download_url = info['requested_formats'][0].get('url')

            if not download_url and 'formats' in info:
                download_url = info['formats'][-1].get('url')

            return jsonify({
                'success': True,
                'data': {
                    'title': info.get('title'),
                    'thumbnail': info.get('thumbnail'),
                    'download_url': download_url
                }
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
