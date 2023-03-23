function startRecognition() {
  // Inicia o reconhecimento de voz
  var recognition = new webkitSpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.lang = "pt-BR";
  recognition.start();

  // Quando uma mensagem é reconhecida, envia para o servidor
  recognition.onresult = function (e) {
    var message = e.results[0][0].transcript;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/send_message", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 200) {
        console.log("Mensagem enviada com sucesso!");
      }
    };
    xhr.send(JSON.stringify({ message: message }));
    recognition.stop();
  };

  // Quando ocorre um erro no reconhecimento, para a gravação
  recognition.onerror = function (e) {
    recognition.stop();
  };
}


// evento que conecta ao WebSocket do servidor e atualiza a tela com as mensagens recebidas do servidor
/*
var socket = io.connect("http://" + document.domain + ":" + location.port);

socket.on("message", function (message) {
  var chatContainer = document.getElementById("chat-container");
  var messageElem = document.createElement("div");
  messageElem.classList.add("message"); // adiciona uma classe ao elemento criado
  messageElem.innerHTML = "<p>" + message + "</p>";
  chatContainer.appendChild(messageElem);
});
*/
