document.addEventListener('DOMContentLoaded', () => {
    const message = "Welcome to Chatbot";
    let i = 0;
    const speed = 100; // Speed of typing effect
    const delay = 1000; // Delay before restarting the typing effect

    function typeWriter() {
        if (i < message.length) {
            document.getElementById("welcome-message").innerHTML += message.charAt(i);
            i++;
            setTimeout(typeWriter, speed);
        } else {
            setTimeout(() => {
                document.getElementById("welcome-message").innerHTML = "";
                i = 0;
                typeWriter();
            }, delay);
        }
    }

    typeWriter();
});
