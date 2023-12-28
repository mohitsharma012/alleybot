

// sidebar code 
function openNav() {
    document.getElementById("mySidebar").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
    document.getElementById("openbtn").style.display = "none";
    document.getElementById("closebtn").style.display = "block"
}

function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("main").style.marginLeft= "0";
    document.getElementById("openbtn").style.display = "block";
    document.getElementById("closebtn").style.display = "none"
}



function speakResponse(responseText) {
    var synth = window.speechSynthesis;
    var utterance = new SpeechSynthesisUtterance(responseText);
    synth.speak(utterance);
}

// Example usage
// Assuming 'ai_response' is the response text you received from the AI




document.addEventListener("DOMContentLoaded", function() {
    let recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;

    document.querySelector('#start-record-btn').addEventListener('click', function(){
        recognition.start();
        document.getElementById('transcript').innerText = "Listening...";
    });

    recognition.onresult = function(event){
        let transcript = event.results[event.resultIndex][0].transcript.trim();
        document.getElementById('transcript').innerText = "You said: " + transcript;
        fetchAIResponse(transcript);
    };

    recognition.onspeechend = function() {
        recognition.stop();
    };

    recognition.onerror = function(event) {
        console.error('Speech recognition error detected: ' + event.error);
    };

    function fetchAIResponse(transcript) {
        fetch('/process_voice/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: 'transcript=' + encodeURIComponent(transcript) 
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('ai-response').innerText = "AI Friend says: " + data.response;
            speakResponse(data.response);  // Speak out the AI response

        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            let cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
