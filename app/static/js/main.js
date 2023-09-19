let chatHistory = [];
let currentConfigId = 'neutral'; // default config
let currentConfigName = 'Neutral'; // default config name

function selectConfig(configId, configName) {
    currentConfigId = configId;
    currentConfigName = configName;
    
    // Clear previous active configuration
    document.querySelectorAll(".config-btn").forEach(btn => {
        btn.classList.remove("active-config");
    });
    
    // Highlight the current selected configuration
    let selectedBtn = document.querySelector(`button[onclick="selectConfig('${configId}', '${configName}')"]`);
    if (selectedBtn) {
        selectedBtn.classList.add("active-config");
    }
}


function submitQuestion() {
    let userInput = document.getElementById("userInput").value;

    chatHistory.push({role: "user", content: userInput});
    
    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'chatHistory': chatHistory,
            'configId': currentConfigId
        }),
    })
    .then(response => response.json())
    .then(data => {
        let chatBox = document.getElementById("chatBox");

        // Render user input as plain text
        chatBox.innerHTML += "<div class='chat-message'><b>" + currentUsername + ":</b> " + userInput + "</div>";

        // Render AI's response with markdown support
        let aiResponse = marked(data.response);  // Convert Markdown to HTML
        aiResponse = DOMPurify.sanitize(aiResponse);  // Sanitize the HTML

        chatBox.innerHTML += "<div class='chat-message'><b>" + currentConfigName + ":</b> " + aiResponse + "</div>";

        chatHistory.push({role: "assistant", content: data.response});
    });

    document.getElementById("userInput").value = "";
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
    
    