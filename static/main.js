const messagesEl = document.getElementById("messages");
const inputEl = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const sendLabel = sendBtn.querySelector(".label");
const statusEl = document.getElementById("status");
const formEl = document.getElementById("chatForm");

const sessionId = getOrCreateSessionId();

function getOrCreateSessionId() {
  const STORAGE_KEY = "chatbot_session_id";
  const existing = sessionStorage.getItem(STORAGE_KEY);
  if (existing) {
    return existing;
  }
  const newId = cryptoRandomId();
  sessionStorage.setItem(STORAGE_KEY, newId);
  return newId;
}

function cryptoRandomId() {
  if (window.crypto && crypto.randomUUID) {
    return crypto.randomUUID();
  }
  return `session-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function formatTimestamp(date = new Date()) {
  return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function appendMessage(role, text) {
  const wrapper = document.createElement("div");
  wrapper.className = `message ${role}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;
  wrapper.appendChild(bubble);

  const time = document.createElement("span");
  time.className = "timestamp";
  time.textContent = formatTimestamp();
  wrapper.appendChild(time);

  messagesEl.appendChild(wrapper);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function setStatus(message, type = "info") {
  statusEl.textContent = message;
  statusEl.dataset.type = type;
}

function setLoading(isLoading) {
  if (isLoading) {
    sendBtn.disabled = true;
    inputEl.disabled = true;
    sendLabel.textContent = "Sending…";
    setStatus("Thinking…", "info");
  } else {
    sendBtn.disabled = false;
    inputEl.disabled = false;
    sendLabel.textContent = "Send";
  }
}

function resetInputHeight() {
  inputEl.style.height = "auto";
  inputEl.style.height = `${Math.min(inputEl.scrollHeight, 160)}px`;
}

async function handleSubmit(event) {
  event.preventDefault();
  const message = inputEl.value.trim();
  if (!message) {
    setStatus("Please type something first.", "error");
    return;
  }

  appendMessage("user", message);
  inputEl.value = "";
  resetInputHeight();

  try {
    setLoading(true);
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, session_id: sessionId }),
    });

    const data = await response.json();
    const reply = data.answer || "(no response)";
    appendMessage("bot", reply);

    if (reply.startsWith("(API error)")) {
      setStatus("OpenAI couldn’t respond. Showing fallback.", "error");
    } else if (reply.startsWith("(offline demo)")) {
      setStatus("OpenAI key missing – running in demo mode.", "info");
    } else {
      setStatus("All good! Ask away.", "success");
    }
  } catch (error) {
    console.error(error);
    appendMessage("bot", "(network error)");
    setStatus("Network error. Please try again.", "error");
  } finally {
    setLoading(false);
    inputEl.focus();
  }
}

function setup() {
  appendMessage(
    "bot",
    "Hey there! I’m your AI assistant. Ask me anything or say hello 👋"
  );
  resetInputHeight();
  inputEl.focus();

  inputEl.addEventListener("input", resetInputHeight);

  inputEl.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      formEl.requestSubmit();
    }
  });

  formEl.addEventListener("submit", handleSubmit);
}

setup();

