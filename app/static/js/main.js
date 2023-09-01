let chatHistory = [];

function submitQuestion() {
        let userInput = document.getElementById("userInput").value;
        let chosenConfig = document.getElementById("aiConfig");
        let chosenConfigName = chosenConfig.options[chosenConfig.selectedIndex].text;

        chatHistory.push({role: "user", content: userInput});  // add user's message to history
        
        fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'chatHistory': chatHistory,
                'configId': chosenConfig.value
            }),
        })
        .then(response => response.json())
        .then(data => {
            let chatBox = document.getElementById("chatBox");
            chatBox.innerHTML += "<div class='chat-message'><b>" + currentUsername + ":</b> " + userInput + "</div>";
            chatBox.innerHTML += "<div class='chat-message'><b>" + chosenConfigName + ":</b> " + data.response + "</div>";
    
            
            chatHistory.push({role: "assistant", content: data.response});  // add AI's response to history
        });

        document.getElementById("userInput").value = ""; // Clear the input field
    }

function updateValue(slider, outputId) {
        document.getElementById(outputId).textContent = slider.value;
    }

document.getElementById('endSessionBtn').addEventListener('click', async function() {
        // Collecting chat history
        const chatHistoryElements = document.querySelectorAll('.chat-message');
        let chatHistoryText = '';
        
        chatHistoryElements.forEach(el => {
            chatHistoryText += el.textContent + '\n';
        });

        // Sending chat history to the server for a summary
        const response = await fetch('/end_session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({chatHistory: chatHistoryText})
        });

        const data = await response.json();

        if (data.success) {
            alert('Session ended and summary saved!');
        } else {
            alert('Error ending session. Please try again.');
        }
    });

function displayReminder(reminder) {
        let chatBox = document.getElementById("chatBox");
        chatBox.innerHTML += "<div><b>AI:</b> " + reminder + "</div>";
    }
    
document.addEventListener("DOMContentLoaded", function() {
        if (reminder) {
            displayReminder(reminder);
        }
    });
    
    