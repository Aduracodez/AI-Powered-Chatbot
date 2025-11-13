const messagesEl = document.getElementById("messages");
const inputEl = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const sendLabel = sendBtn.querySelector(".label");
const statusEl = document.getElementById("status");
const formEl = document.getElementById("chatForm");
const languageSelect = document.getElementById("languageSelect");

const translations = {
  en: {
    greeting: "Hey there! I’m your AI assistant. Ask me anything or say hello 👋",
    placeholder: "Type a message…",
    labelSend: "Send",
    labelSending: "Sending…",
    statusReady: "Ready to chat ✨",
    statusThinking: "Thinking…",
    statusEmpty: "Please type something first.",
    statusNetworkError: "Network error. Please try again.",
    statusOffline: "OpenAI key missing – running in demo mode.",
    statusApiError: "OpenAI couldn’t respond. Showing fallback.",
    statusSuccess: "All good! Ask away.",
    languageChanged: "Got it! I’ll reply in English.",
    languageChangedPrompt: "Language updated to English.",
  },
  de: {
    greeting: "Hallo! Ich bin deine KI-Assistentin. Stell mir eine Frage oder sag Hallo 👋",
    placeholder: "Schreibe eine Nachricht…",
    labelSend: "Senden",
    labelSending: "Sende…",
    statusReady: "Bereit zum Chatten ✨",
    statusThinking: "Ich denke nach…",
    statusEmpty: "Bitte schreibe zuerst etwas.",
    statusNetworkError: "Netzwerkfehler. Bitte versuche es erneut.",
    statusOffline: "OpenAI-Schlüssel fehlt – Demo-Modus aktiv.",
    statusApiError: "OpenAI konnte nicht antworten. Zeige Fallback.",
    statusSuccess: "Alles gut! Stell deine Frage.",
    languageChanged: "Alles klar! Ich antworte jetzt auf Deutsch.",
    languageChangedPrompt: "Sprache auf Deutsch umgestellt.",
  },
};

let currentLanguage = languageSelect?.value || "en";
const sessionId = getOrCreateSessionId();

function t(key) {
  const catalog = translations[currentLanguage] || translations.en;
  return catalog[key] ?? key;
}

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
    sendLabel.textContent = t("labelSending");
    setStatus(t("statusThinking"), "info");
  } else {
    sendBtn.disabled = false;
    inputEl.disabled = false;
    sendLabel.textContent = t("labelSend");
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
    setStatus(t("statusEmpty"), "error");
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
      body: JSON.stringify({
        message,
        session_id: sessionId,
        language: currentLanguage,
      }),
    });

    const data = await response.json();
    const reply = data.answer || "(no response)";
    appendMessage("bot", reply);

    switch (data.mode) {
      case "offline":
        setStatus(t("statusOffline"), "info");
        break;
      case "error":
        setStatus(t("statusApiError"), "error");
        break;
      default:
        setStatus(t("statusSuccess"), "success");
        break;
    }
  } catch (error) {
    console.error(error);
    appendMessage("bot", "(network error)");
    setStatus(t("statusNetworkError"), "error");
  } finally {
    setLoading(false);
    inputEl.focus();
  }
}

function applyLanguageSettings() {
  inputEl.placeholder = t("placeholder");
  sendLabel.textContent = t("labelSend");
  if (!statusEl.textContent) {
    setStatus(t("statusReady"), "info");
  }
}

function handleLanguageChange(event) {
  currentLanguage = event.target.value;
  const message = t("languageChanged");
  applyLanguageSettings();
  setStatus(t("languageChangedPrompt"), "success");
  appendMessage("bot", message);
  inputEl.focus();
}

function setup() {
  applyLanguageSettings();
  appendMessage("bot", t("greeting"));
  resetInputHeight();
  inputEl.focus();

  inputEl.addEventListener("input", resetInputHeight);
  formEl.addEventListener("submit", handleSubmit);

  inputEl.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      formEl.requestSubmit();
    }
  });

  languageSelect.addEventListener("change", handleLanguageChange);
}

setup();

