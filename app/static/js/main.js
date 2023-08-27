let chatHistory = [];

function submitQuestion() {
    let userInput = document.getElementById("userInput").value;
    let chosenConfigId = document.getElementById("aiConfig").value;
    chatHistory.push({role: "user", content: userInput});  // add user's message to history
    
    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'chatHistory': chatHistory,
            'configId': chosenConfigId
        }),
    })
    .then(response => response.json())
    .then(data => {
        let chatBox = document.getElementById("chatBox");
        chatBox.innerHTML += "<div><b>You:</b> " + userInput + "</div>";
        chatBox.innerHTML += "<div><b>AI:</b> " + data.response + "</div>";
        
        chatHistory.push({role: "assistant", content: data.response});  // add AI's response to history
    });

    document.getElementById("userInput").value = ""; // Clear the input field
}

function updateValue(slider, outputId) {
    document.getElementById(outputId).textContent = slider.value;
}
