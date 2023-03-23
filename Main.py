from flask import Flask, render_template, redirect, url_for, request, jsonify
import openai
import requests
from openai_IA import get_openai_response
from speech import transcription
from chatbot import chatbot
from auth import login, register, home
#from send_message import send_message

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'PRIVATE'
openai.api_key = "PRIVATE"


# Cria o histórico de mensagens
messages = []

# Define as rotas para login, registro e home
app.route('/', methods=['GET', 'POST'])(login)
app.route('/register', methods=['GET', 'POST'])(register)
app.route('/home')(home)
app.route('/transcription', methods=['POST'])
app.route("/send_message", methods=["POST"])
#socketio.on('message') waiting ...


if __name__ == '__main__':
    app.run(debug=True)
