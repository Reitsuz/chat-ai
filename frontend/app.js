async function send() {
    let input = document.getElementById("text");
    let text = input.value;

    if (!text) return;

    addMessage(text, "user");
    input.value = "";

    let res = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({text})
    });

    let data = await res.json();

    addMessage(data.reply, "ai");
}

function addMessage(text, type) {
    let div = document.createElement("div");
    div.className = "msg " + type;
    div.innerText = text;

    document.getElementById("chat").appendChild(div);

    window.scrollTo(0, document.body.scrollHeight);
}