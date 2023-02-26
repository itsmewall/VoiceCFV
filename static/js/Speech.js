function startDictation() {
    if (window.hasOwnProperty("webkitSpeechRecognition")) {
  
      var recognition = new webkitSpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = "pt-BR";
      recognition.start();
  
      recognition.onresult = function (e) {
        document.getElementById("transcript").value = e.results[0][0].transcript;
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/transcription", true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onreadystatechange = function () {
          if (xhr.readyState === 4 && xhr.status === 200) {
            console.log("Transcrição salva com sucesso!");
            console.log("Transcrição: ", e.results[0][0].transcript); // adiciona essa linha para exibir a transcrição no console log do navegador
          }
        };
        xhr.send(JSON.stringify({ text: e.results[0][0].transcript }));
        recognition.stop();
      };
      recognition.onerror = function (e) {
        recognition.stop();
      };
    }
  }
  