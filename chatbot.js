const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const typingIndicator = document.getElementById('typing-indicator');
const downloadTemplateButton = document.getElementById('download-template');
const clearChatButton = document.getElementById('clear-chat');
const darkModeToggle = document.getElementById('dark-mode-toggle');

// Send message to the backend
sendButton.addEventListener('click', () => {
    const message = userInput.value;
    if (message.trim() !== '') {
        displayMessage(message, 'user');
        userInput.value = '';
        getAIResponse(message);
    }
});

// Display messages in chat
function displayMessage(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${sender}-message`);
    messageDiv.textContent = message;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Get AI response from the server
async function getAIResponse(userMessage) {
    typingIndicator.style.display = 'block';
    try {
        const response = await fetch('http://127.0.0.1:5001/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userMessage }),
        });
        const data = await response.json();
        if (data && data.response) {
            displayMessage(data.response, 'bot');
        } else {
            displayMessage("Sorry, I couldn't understand that.", 'bot');
        }
    } catch (error) {
        displayMessage("I'm sorry, I couldn't process your request. Please try again later.", 'bot');
    } finally {
        typingIndicator.style.display = 'none';
    }
}

// Dark Mode Toggle
darkModeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
});

// On page load, check if dark mode was previously enabled
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
}

// Clear Chat
clearChatButton.addEventListener('click', () => {
    chatContainer.innerHTML = '';
});

// Download Template Button
downloadTemplateButton.addEventListener('click', () => {
    window.location.href = '/download/template'; // Adj,nust the URL to your backend's template download endpoint
});
