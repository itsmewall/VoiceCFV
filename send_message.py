from flask import Flask, request
import socketio

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'PRIVATE'

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