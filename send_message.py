from flask import Flask, request
import socketio
from flask_socketio import SocketIO, send

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'PRIVATE'
socketio = SocketIO(app)

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    send(message, broadcast=True)

# Cria o histórico de mensagens
messages = []

@app.route("/send_message", methods=["POST"])
def send_message():
    # Recebe a mensagem do cliente
    message = request.json["message"]
    
    # Adiciona a mensagem ao histórico de mensagens
    messages.append(message)
    
    # Envia a mensagem para todos os clientes conectados
    socketio.emit("message", message)
    return "OK"


if __name__ == '__main__':
    app.run(debug=True)