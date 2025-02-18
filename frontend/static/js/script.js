/* File: static/js/script.js */
function toggleChat() {
    var chatPopup = document.getElementById("chatPopup");
    chatPopup.style.display = chatPopup.style.display === "block" ? "none" : "block";
}

function sendMessage() {
    let inputField = document.getElementById("chatMessage");
    let messageText = inputField.value.trim();

    if (messageText !== "") {
        let chatBody = document.querySelector(".chat-body");
        let newMessage = document.createElement("div");
        newMessage.classList.add("chat-message");
        newMessage.textContent = messageText;

        chatBody.appendChild(newMessage);
        inputField.value = ""; // Clear input after sending

        // Scroll to bottom
        chatBody.scrollTop = chatBody.scrollHeight;
    }
}
