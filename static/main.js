const appConfig = window.appConfig || {};
const messagesEl = document.getElementById("messages");
const inputEl = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const sendLabel = sendBtn.querySelector(".label");
const statusEl = document.getElementById("status");
const formEl = document.getElementById("chatForm");
const languageSelect = document.getElementById("languageSelect");
const providerSelect = document.getElementById("providerSelect");
const modelSelect = document.getElementById("modelSelect");
const modelPicker = document.getElementById("modelPicker");

const modelOptions = appConfig.modelOptions || {};
const defaultModels = appConfig.defaultModels || {};
const localLLMEnabled = appConfig.localLLMEnabled ?? false;
const groqEnabled = appConfig.groqEnabled ?? false;

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
    statusOffline: "Provider key missing – running in demo mode.",
    statusApiError: "The provider couldn’t respond. Showing fallback.",
    statusSuccess: "All good! Ask away.",
    statusLocalDisabled: "Local model is not enabled. Please start the service or pick OpenAI.",
    statusLocalError: "Local model failed. See logs and try again.",
    statusGroqDisabled: "Groq isn’t configured yet. Add GROQ_API_KEY or switch providers.",
    providerOpenAI: "OpenAI",
    providerLocal: "Local LLM",
    providerGroq: "Groq",
    providerOpenAINotice: "Using OpenAI (requires API key).",
    providerLocalNotice: localLLMEnabled
      ? "Using the local model. Make sure Ollama is running."
      : "Local model currently disabled.",
    providerGroqNotice: groqEnabled
      ? "Using Groq (Llama 3)."
      : "Groq API key missing – set GROQ_API_KEY.",
    languageChanged: "Got it! I’ll reply in English.",
    languageChangedPrompt: "Language updated to English.",
    modelChanged: "Model switched to {model}.",
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
    statusOffline: "Provider-Schlüssel fehlt – Demo-Modus aktiv.",
    statusApiError: "Der Anbieter konnte nicht antworten. Zeige Fallback.",
    statusSuccess: "Alles gut! Stell deine Frage.",
    statusLocalDisabled: "Lokales Modell nicht aktiviert. Starte den Dienst oder wähle OpenAI.",
    statusLocalError: "Lokales Modell fehlgeschlagen. Prüfe die Logs und versuche es erneut.",
    statusGroqDisabled: "Groq ist nicht konfiguriert. Setze GROQ_API_KEY oder wähle einen anderen Provider.",
    providerOpenAI: "OpenAI",
    providerLocal: "Lokales LLM",
    providerGroq: "Groq",
    providerOpenAINotice: "Verwende OpenAI (API-Schlüssel erforderlich).",
    providerLocalNotice: localLLMEnabled
      ? "Verwende das lokale Modell. Stelle sicher, dass Ollama läuft."
      : "Lokales Modell derzeit deaktiviert.",
    providerGroqNotice: groqEnabled
      ? "Verwende Groq (Llama 3)."
      : "Groq-API-Schlüssel fehlt – setze GROQ_API_KEY.",
    languageChanged: "Alles klar! Ich antworte jetzt auf Deutsch.",
    languageChangedPrompt: "Sprache auf Deutsch umgestellt.",
    modelChanged: "Modell zu {model} gewechselt.",
  },
};

let currentLanguage = languageSelect?.value || "en";
let currentProvider = appConfig.defaultProvider || "openai";
let currentModel = defaultModels[currentProvider] ||
  (modelOptions[currentProvider] || [])[0]?.id || "";
const sessionId = getOrCreateSessionId();

function t(key) {
  const catalog = translations[currentLanguage] || translations.en;
  return catalog[key] ?? key;
}

function format(key, vars = {}) {
  const template = t(key);
  return template.replace(/\{(\w+)\}/g, (_, name) => vars[name] ?? "");
}

function providerLabel(providerId) {
  if (providerId === "local") {
    return t("providerLocal");
  }
  if (providerId === "groq") {
    return t("providerGroq");
  }
  return t("providerOpenAI");
}

function providerNoticeKey(providerId) {
  if (providerId === "local") return "providerLocalNotice";
  if (providerId === "groq") return "providerGroqNotice";
  return "providerOpenAINotice";
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

function populateProviderSelect() {
  providerSelect.innerHTML = "";
  Object.keys(modelOptions).forEach((providerId) => {
    const option = document.createElement("option");
    option.value = providerId;
    option.textContent = providerLabel(providerId);
    providerSelect.appendChild(option);
  });
  providerSelect.value = currentProvider;
}

function populateModelSelect() {
  const options = modelOptions[currentProvider] || [];
  modelSelect.innerHTML = "";
  if (!options.length) {
    modelPicker.style.display = "none";
    currentModel = "";
    return;
  }
  modelPicker.style.display = "inline-flex";
  options.forEach(({ id, label }) => {
    const option = document.createElement("option");
    option.value = id;
    option.textContent = label;
    modelSelect.appendChild(option);
  });
  if (!options.some(({ id }) => id === currentModel)) {
    currentModel = defaultModels[currentProvider] || options[0].id;
  }
  modelSelect.value = currentModel;
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
        provider: currentProvider,
        model: currentModel,
      }),
    });

    const data = await response.json();
    const reply = data.answer || "(no response)";
    appendMessage("bot", reply);

    updateInsights(data.mode);
    switch (data.mode) {
      case "offline":
        setStatus(t("statusOffline"), "info");
        break;
      case "error":
        setStatus(t("statusApiError"), "error");
        break;
      case "local_disabled":
        setStatus(t("statusLocalDisabled"), "error");
        break;
      case "local_error":
        setStatus(t("statusLocalError"), "error");
        break;
      case "groq_disabled":
        setStatus(t("statusGroqDisabled"), "error");
        break;
      default:
        setStatus(t("statusSuccess"), "success");
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
  applyLanguageSettings();
  updateInsights();
  setStatus(t("languageChangedPrompt"), "success");
  appendMessage("bot", t("languageChanged"));
  inputEl.focus();
}

function handleProviderChange(event) {
  currentProvider = event.target.value;
  currentModel = defaultModels[currentProvider] ||
    (modelOptions[currentProvider] || [])[0]?.id || "";
  populateModelSelect();
  const noticeKey = providerNoticeKey(currentProvider);
  const isError =
    (currentProvider === "local" && !localLLMEnabled) ||
    (currentProvider === "groq" && !groqEnabled);
  setStatus(t(noticeKey), isError ? "error" : "info");
  updateInsights();
  inputEl.focus();
}

function handleModelChange(event) {
  currentModel = event.target.value;
  setStatus(format("modelChanged", { model: event.target.selectedOptions[0]?.textContent || currentModel }), "info");
  inputEl.focus();
}

const providerInsightEl = document.getElementById("insight-provider");
const languageInsightEl = document.getElementById("insight-language");
const modeInsightEl = document.getElementById("insight-mode");

function updateInsights(modeLabel) {
  if (providerInsightEl) providerInsightEl.textContent = providerLabel(currentProvider);
  if (languageInsightEl) languageInsightEl.textContent = currentLanguage.toUpperCase();
  if (modeInsightEl) {
    modeInsightEl.textContent = (modeLabel || "Live").replace(/_/g, " ");
  }
}

function setup() {
  applyLanguageSettings();
  populateProviderSelect();
  populateModelSelect();
  appendMessage("bot", t("greeting"));
  resetInputHeight();
  inputEl.focus();
  updateInsights();

  inputEl.addEventListener("input", resetInputHeight);
  formEl.addEventListener("submit", handleSubmit);

  inputEl.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      formEl.requestSubmit();
    }
  });

  languageSelect.addEventListener("change", handleLanguageChange);
  providerSelect.addEventListener("change", handleProviderChange);
  modelSelect.addEventListener("change", handleModelChange);
}

setup();

