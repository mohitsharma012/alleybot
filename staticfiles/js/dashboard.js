
// Function to handle speech synthesis
function speakResponse(responseText) {
    var synth = window.speechSynthesis;
    var utterance = new SpeechSynthesisUtterance(responseText);

    // Set properties for pitch and rate
    utterance.pitch = 1.2;
    utterance.rate = 1;

    // Select a female voice
    var voices = synth.getVoices();
    var allyVoice = voices.find(voice => voice.gender === 'female');
    if (allyVoice) {
        utterance.voice = allyVoice;
    } else {
        console.log("Female voice not found. Using default voice.");
    }

    // Event listener for when speaking ends
    utterance.onend = function(event) {
        console.log('Speaking has stopped.');
        startListening(); // Restart listening after speaking
    };

    // Speak the text
    synth.speak(utterance);
}

// Function to start speech recognition
function startListening() {
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;

    recognition.start();
    document.getElementById('transcript').innerText = "Listening...";
    document.getElementById('start-record-btn').innerText = "Listening...";

    recognition.onresult = function(event) {
        if (event.results[event.resultIndex].isFinal) {
            let transcript = event.results[event.resultIndex][0].transcript.trim();
            document.getElementById('transcript').innerText = "You said: " + transcript;
            fetchAIResponse(transcript);
        }
    };

    recognition.onspeechend = function() {
        recognition.stop();
        document.getElementById('transcript').innerText = "Click Here to Speak";
        document.getElementById('start-record-btn').innerText = "Click Here to Speak";
    };

    recognition.onerror = function(event) {
        console.error('Speech recognition error: ' + event.error);
    };
}

// Function to fetch response from AI (or any backend processing)
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
        document.getElementById('ai-response').innerText = "Alley: " + data.response;
        speakResponse(data.response); // Speak out the AI response
    });
}

// Helper function to get CSRF token
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

// Initialize the application
document.addEventListener("DOMContentLoaded", function() {
    document.querySelector('#start-record-btn').addEventListener('click', function() {
        startListening(); // Start listening when the button is clicked
    });
});
