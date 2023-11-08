from flask import Flask, request, jsonify
from pytube import YouTube
import os
import uuid
import whisper

app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe_video():
    try:
        video_url = request.json.get('video_url')

        if not video_url:
            return jsonify({"error": "Missing 'video_url' in the request."}), 400

        yt = YouTube(video_url)
        audio_stream = yt.streams.filter(only_audio=True).first()

        download_path = 'Downloads_Audio'  
        os.makedirs(download_path, exist_ok=True)

        audio_filename = f'audio_{str(uuid.uuid4())[:8]}.mp3'
        audio_file_path = os.path.join(download_path, audio_filename)
        audio_stream.download(output_path=download_path, filename=audio_filename)
        print("Audio file path:", audio_file_path)

        model = whisper.load_model("base")
        print("modle here ")
        result = model.transcribe(audio_file_path)
        print("result here with file")
        text_result = result["text"]
        with open("new.txt", "w") as f:
            f.write(text_result)


        print("text result is here kidnly check")
        return jsonify({"transcription": text_result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
