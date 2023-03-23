from flask import Flask, request, jsonify
import speech_recognition as sr
import openai_IA

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'PRIVATE'
openai_IA.api_key = "PRIVATE"


@app.route('/transcription', methods=['POST'])
def transcription():
    r = sr.Recognizer()
    data = request.get_json()
    audio_data = data['audio']
    try:
        # convert audio data to audio file
        with open("audio.wav", "wb") as f:
            f.write(audio_data)
        # transcribe audio file
        with sr.AudioFile("audio.wav") as source:
            audio_text = r.record(source)
            transcription = r.recognize_google(audio_text, language='en-US')
            # get OpenAI response
            openai_response = openai_IA.get_openai_response(transcription)
            # return response as JSON
            return jsonify({'success': True, 'transcription': transcription, 'openai_response': openai_response}), 200
    except:
        return jsonify({'success': False}), 500
    
    
if __name__ == '__main__':
    app.run(debug=True)
