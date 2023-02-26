$(document).ready(function() {
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "pt-BR";
    var conversation = $("#conversation");

    recognition.onresult = function(event) {
        var interim_transcript = "";
        for (var i = event.resultIndex; i < event.results.length; i++) {
            if (event.results[i].isFinal) {
                var final_transcript = event.results[i][0].transcript;
                $("#transcript").val(final_transcript);
                $.ajax({
                    url: '/transcription',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({'text': final_transcript}),
                    success: function(data) {
                        var response = data.response;
                        conversation.append("<div class='user-msg'>" + final_transcript + "</div>");
                        conversation.append("<div class='bot-msg'>" + response + "</div>");
                    },
                    error: function() {
                        console.log('Error');
                    }
                });
            } else {
                interim_transcript += event.results[i][0].transcript;
            }
        }
        $("#interim").val(interim_transcript);
    };

    recognition.start();
});
