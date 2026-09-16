from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/fetch', methods=['POST'])
def fetch_video():
    data = request.get_json()
    video_url = data.get('url')
    format_type = data.get('format', 'video')

    if not video_url:
        return jsonify({'error': 'Please provide a valid YouTube URL.'}), 400

    # Flexible format specifier that NEVER throws "Requested format not available"
    if format_type == 'audio':
        format_selector = 'bestaudio/best'
    else:
        # Tries combined best, then best single stream, then fallback to anything available
        format_selector = 'best[ext=mp4]/best/bestvideo+bestaudio'

    ydl_opts = {
    'format': format_selector,
    'quiet': True,
    'no_warnings': True,
    'format_sort': ['res', 'ext:mp4:m4a'],
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
            
            # Extract streaming direct URL safely
            download_url = info.get('url')
            
            # If YouTube splits formats, grab the first usable direct URL
            if not download_url and 'requested_formats' in info and len(info['requested_formats']) > 0:
                download_url = info['requested_formats'][0].get('url')
                
            # Final fallback to formats list if needed
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
