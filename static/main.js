const box = document.getElementById("messages");
const input = document.getElementById("userInput");
const btn = document.getElementById("sendBtn");

function add(role, text) {
  const p = document.createElement("p");
  p.className = role;
  p.innerText = (role === "user" ? "You: " : "Bot: ") + text;
  box.appendChild(p);
  box.scrollTop = box.scrollHeight;
}

async function sendMessage() {
  const msg = input.value.trim();
  if (!msg) return;
  add("user", msg);
  input.value = "";
  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ message: msg })
    });
    const data = await res.json();
    add("bot", data.answer || "(no response)");
  } catch (e) {
    add("bot", "(network error)");
  }
}

btn.addEventListener("click", sendMessage);
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendMessage();
});

