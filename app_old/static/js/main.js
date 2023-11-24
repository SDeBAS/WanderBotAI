$(document).ready(function () {
    const chatOutput = $('#chat-output');
    const userInput = $('#user-input');
    const voiceInputButton = $('#voice-input');
    const synth = window.speechSynthesis; // Access the SpeechSynthesis API

    function addMessage(message, isUser) {
        const messageClass = isUser ? 'user-message' : 'bot-message';
        chatOutput.append(`<div class="message ${messageClass}">${message}</div>`);
    }

    function speakMessage(message) {
        const speechMessage = new SpeechSynthesisUtterance(message);
        synth.speak(speechMessage);
    }

    const recognition = new webkitSpeechRecognition();

    recognition.onresult = function (event) {
        const userMessage = event.results[0][0].transcript;
        userInput.val(userMessage);
        sendUserMessage(userMessage);
    };

    voiceInputButton.click(function () {
        recognition.start();
    });

    function sendUserMessage(userMessage) {
        addMessage(userMessage, true);

        $.ajax({
            url: '/chat',
            type: 'POST',
            data: { user_input: userMessage },
            success: function (data) {
                const botResponse = data.bot_response;
                addMessage(botResponse, false);
                speakMessage(botResponse); // Speak the bot's response
            }
        });
    }

    userInput.keypress(function (event) {
        if (event.which === 13) {
            event.preventDefault();
            const userMessage = userInput.val();
            sendUserMessage(userMessage);
            userInput.val('');
        }
    });
});
