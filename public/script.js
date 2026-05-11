// Simple Agent Frontend JavaScript

document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');
    
    // Store conversation history
    let conversationHistory = [];
    
    // Add a message to the chat
    function addMessage(content, type = 'assistant') {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', type);
        
        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        contentDiv.textContent = content;
        
        const timeDiv = document.createElement('div');
        timeDiv.classList.add('message-time');
        timeDiv.textContent = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        
        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(timeDiv);
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Handle sending a message
    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;
        
        // Disable input while processing
        userInput.disabled = true;
        sendButton.disabled = true;
        sendButton.textContent = 'Processing...';
        
        // Add user message to chat
        addMessage(message, 'user');
        userInput.value = '';
        
        try {
            // Call the agent API
            const response = await fetch('/.netlify/functions/simple-agent', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    history: conversationHistory
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Add agent response to chat
            addMessage(data.response, 'assistant');
            
            // Update conversation history
            conversationHistory = data.history;
            
        } catch (error) {
            console.error('Error:', error);
            addMessage('Sorry, I encountered an error processing your request. Please try again.', 'assistant');
        } finally {
            // Re-enable input
            userInput.disabled = false;
            sendButton.disabled = false;
            sendButton.textContent = 'Send';
            userInput.focus();
        }
    }
    
    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Focus input on load
    userInput.focus();
    
    // Add welcome message
    addMessage('Hello! I am a Simple Agent that follows the perception-reasoning-action-memory loop. I can help you with questions, calculations, and more. Try asking me something like: "What is the weather in Tokyo?", "Calculate 15 * 23", or "Search for information about machine learning."', 'assistant');
});