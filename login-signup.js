document.addEventListener('DOMContentLoaded', () => {
    const message = "Welcome to Chatbot";
    let i = 0;
    const speed = 170; // Speed of typing effect
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

function signIn() {
    let oauthendpoint = "https://accounts.google.com/o/oauth2/v2/auth"

    let form = document.createElement('form')
    form.setAttribute('method', 'GET')
    form.setAttribute('action',oauthendpoint)

    let params = {
        "client_id" : "133402870707-nhuffft968a6jolttuq1b2b6jg42rk3p.apps.googleusercontent.com",
        "redirect_uri" : "http://127.0.0.1:8000/",
        "response_type" : "token",
        "scope" : "https://www.googleapis.com/auth/drive.metadata.readonly",
        "include_granted_scopes" : "true",
        "state" : "pass-through-value"
    }

    for(var p in params){
        let input = document.createElement('input')
        input.setAttribute('type', 'hidden')
        input.setAttribute('name', p)
        input.setAttribute('value', params[p])
        form.appendChild(input)
    }

    document.body.appendChild(form)
    form.submit()
}
