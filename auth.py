from flask import Flask, render_template, redirect, url_for, request, jsonify
import json
import speech_recognition as sr
import openai
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
openai.api_key = "PRIVATE"

# Definindo um dicionário vazio para armazenar os usuários cadastrados
users = {}

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
            return redirect(url_for('home'))
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
    text = data['text']
    try:
        with open("transcription.txt", "a") as f:
            f.write(text + "\n")
        with open("transcription.txt", "r") as f:
            contents = f.read()
            print(contents)
        return jsonify({'success': True}), 200
    except:
        return jsonify({'success': False}), 500


# OPENAI
def get_openai_response(transcription):
    url = "https://api.openai.com/v1/engines/davinci-codex/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }
    data = {
        "prompt": f"Transcription: {transcription}",
        "max_tokens": 60,
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["text"]

# Rota para a página home
@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
