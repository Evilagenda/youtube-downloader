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

    if not video_url:
        return jsonify({'error': 'Please provide a valid YouTube URL'}), 400

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'cookiefile': 'cookies.txt',
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web']
            }
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            download_url = info.get('url')

            if not download_url and 'formats' in info and len(info['formats']) > 0:
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
