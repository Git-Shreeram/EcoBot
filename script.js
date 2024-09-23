async function sendMessage() {
    const messageInput = document.getElementById("messageInput");
    const userMessage = messageInput.value;
    messageInput.value = "";

    try {
        const response = await fetch("/api/messages", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: userMessage })
        });

        const data = await response.json();
        const botResponse = data.response;

        const chatContainer = document.getElementById("chatContainer");
        chatContainer.innerHTML += `<div><strong>You:</strong> ${userMessage}</div>`;
        chatContainer.innerHTML += `<div><strong>Bot:</strong> ${botResponse}</div>`;
    } catch (error) {
        console.error("Error sending message:", error);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const sendButton = document.getElementById("sendButton");
    sendButton.addEventListener("click", sendMessage);
});
