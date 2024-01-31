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

    // Update URL to reflect the current configuration without triggering a page reload
    window.history.pushState(null, null, `/chat?config_id=${configId}`);

    // Send an initial query with the chosen configuration
    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'chatHistory': [],
            'configId': currentConfigId
        }),
    })
    .then(response => response.json())
    .then(data => {
        let chatBox = document.getElementById("chatBox");
        
        // Render AI's response with markdown support
        let aiResponse = marked(data.response);  // Convert Markdown to HTML
        aiResponse = DOMPurify.sanitize(aiResponse);  // Sanitize the HTML
        
        chatBox.innerHTML += "<div class='chat-message'><b>" + currentConfigName + ":</b> " + aiResponse + "</div>";
        scrollToBottom();
        chatHistory.push({role: "assistant", content: data.response});
    });
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
        scrollToBottom();
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
        body: JSON.stringify({
            chatHistory: chatHistoryText,
            configId: currentConfigId  // Including configId here
        })
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
    
    window.addEventListener('popstate', function(event) {
        // Extract configId from the current URL
        let urlSegments = window.location.pathname.split('/');
        let configIdFromURL = urlSegments[urlSegments.length - 1];
    
        // If the extracted configId is different from currentConfigId, then call selectConfig
        if (configIdFromURL !== currentConfigId) {
            selectConfig(configIdFromURL, configIdFromURL.charAt(0).toUpperCase() + configIdFromURL.slice(1));
        }
    });
    
    function scrollToBottom() {
        var chatBox = document.getElementById("chatBox");
        chatBox.scrollTop = chatBox.scrollHeight;
    }
    