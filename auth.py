from flask import Flask, render_template, redirect, url_for, request, jsonify
import socketio
import speech_recognition as sr
import openai
import requests

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'PRIVATE'
openai.api_key = "PRIVATE"

# Definindo um dicionário vazio para armazenar os usuários cadastrados
users = {}

# Cria o histórico de mensagens
messages = []

# Rota para a página de login
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users:
            error = 'Usuário não existe'
        elif users[username]['password'] != password:
            error = 'Senha incorreta'
        else:
            # Se as credenciais estiverem corretas, redireciona para a página home
            return redirect(url_for('home', username=username))
    
    return render_template('login.html', error=error)

# Rota para a página de cadastro
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if username in users:
            error = 'Usuário já existe'
        elif password != confirm_password:
            error = 'Senhas não coincidem'
        else:
            # Adiciona o usuário ao dicionário de usuários
            users[username] = {'password': password}
            # Redireciona para a página de login
            return redirect(url_for('login'))
    return render_template('register.html', error=error)

# SPEECH
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
            openai_response = get_openai_response(transcription)
            # return response as JSON
            return jsonify({'success': True, 'transcription': transcription, 'openai_response': openai_response}), 200
    except:
        return jsonify({'success': False}), 500

@app.route("/send_message", methods=["POST"])
def send_message():
    # Recebe a mensagem do cliente
    message = request.json["message"]
    
    # Adiciona a mensagem ao histórico de mensagens
    messages.append(message)
    
    # Envia a mensagem para todos os clientes conectados
    socketio.emit("message", message)
    
    return "OK"


# OPENAI
def get_openai_response(prompt):
    url = "https://api.openai.com/v1/engines/davinci-codex/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 60,
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["text"]


# Rota para a página home
@app.route('/home')
def home():
    username = request.args.get('username')
    return render_template('home.html', username=username)


if __name__ == '__main__':
    app.run(debug=True)
