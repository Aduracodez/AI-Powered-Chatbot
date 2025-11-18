from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from models import db, Conversation
import requests

load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    f'sqlite:///{os.path.join(basedir, "chatbot.db")}'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

SUPPORTED_LANGUAGES = {
    "en": {
        "label": "English",
        "system_prompt": (
            "You are a friendly, concise chatbot. "
            "Always respond in English and keep answers brief yet helpful. "
            "If the user writes in another language, translate their request first, "
            "then answer in English."
        ),
        "offline_template": "(offline demo) You said: {message}",
        "api_error_template": "(API error) {error}",
        "local_disabled_template": (
            "(local model unavailable) Enable the local LLM service or choose OpenAI."
        ),
        "local_error_template": "(Local model error) {error}",
        "groq_disabled_template": "(Groq disabled) Add a GROQ_API_KEY or choose another provider.",
    },
    "de": {
        "label": "German",
        "system_prompt": (
            "Du bist ein freundlicher, prägnanter Chatbot. "
            "Antworte ausschließlich auf Deutsch und halte Antworten hilfreich und knapp. "
            "Wenn die Nutzerinnen oder Nutzer in einer anderen Sprache schreiben, "
            "übersetze die Anfrage zuerst und antworte dann auf Deutsch."
        ),
        "offline_template": "(Offline-Demo) Du hast gesagt: {message}",
        "api_error_template": "(API-Fehler) {error}",
        "local_disabled_template": (
            "(Lokales Modell nicht verfügbar) Aktiviere den lokalen Dienst oder wähle OpenAI."
        ),
        "local_error_template": "(Fehler im lokalen Modell) {error}",
        "groq_disabled_template": "(Groq deaktiviert) Hinterlege einen GROQ_API_KEY oder wähle einen anderen Provider.",
    },
}
DEFAULT_LANGUAGE = "en"

OPENAI_MODELS = [
    {
        "id": os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        "label": "GPT-3.5 Turbo",
    }
]
DEFAULT_OPENAI_MODEL = OPENAI_MODELS[0]["id"]

GROQ_MODELS = [
    {
        "id": os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
        "label": os.getenv("GROQ_MODEL_LABEL", "Llama 3.1 8B (Groq)"),
    }
]
DEFAULT_GROQ_MODEL = GROQ_MODELS[0]["id"]

LOCAL_LLM_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")

LOCAL_MODELS = {
    os.getenv("LOCAL_LLM_MODEL", "llama2"):
        {
            "label": os.getenv("LOCAL_LLM_LABEL", "LLaMA 2 (via Ollama)"),
            "provider": "ollama",
        }
}
DEFAULT_LOCAL_MODEL = next(iter(LOCAL_MODELS.keys()))


def str_to_bool(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def detect_local_llm_enabled() -> bool:
    env_toggle = os.getenv("ENABLE_LOCAL_LLM")
    if env_toggle is not None:
        return str_to_bool(env_toggle)

    # Auto-detect by pinging the Ollama API (or compatible local server)
    try:
        response = requests.get(
            f"{LOCAL_LLM_URL.rstrip('/')}/api/tags",
            timeout=1.5,
        )
        return response.ok
    except Exception:
        return False


LOCAL_LLM_ENABLED = detect_local_llm_enabled()

MODEL_OPTIONS = {
    "openai": OPENAI_MODELS,
    "groq": GROQ_MODELS,
    "local": [
        {"id": model_id, "label": meta["label"]}
        for model_id, meta in LOCAL_MODELS.items()
    ],
}
DEFAULT_PROVIDER = os.getenv("DEFAULT_MODEL_PROVIDER", "openai")
if DEFAULT_PROVIDER not in MODEL_OPTIONS:
    DEFAULT_PROVIDER = "openai"
DEFAULT_MODELS = {
    "openai": DEFAULT_OPENAI_MODEL,
    "groq": DEFAULT_GROQ_MODEL,
    "local": DEFAULT_LOCAL_MODEL,
}

# Only use OpenAI if a key is present (so the UI still works without a key) 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = None
if OPENAI_API_KEY:
    try:
        from openai import OpenAI
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
    except Exception:
        openai_client = None  # fall back gracefully

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = None
if GROQ_API_KEY:
    try:
        from groq import Groq
        groq_client = Groq(api_key=GROQ_API_KEY)
    except ImportError:
        # Groq package not installed - that's okay, just disable Groq
        groq_client = None
        print("Warning: groq package not installed. Groq provider will be unavailable.")
    except Exception:
        groq_client = None


def build_system_prompt(language_data, user_msg):
    """Construct a prompt for local LLMs using the language-specific system instructions."""
    return (
        f"{language_data['system_prompt']}\n\n"
        f"User: {user_msg}\n"
        "Assistant:"
    )


def call_local_llm(prompt: str, model_id: str) -> str:
    """Call a locally hosted LLM (e.g., via Ollama)."""
    if not LOCAL_LLM_ENABLED:
        raise RuntimeError("Local LLM not enabled")

    model_id = model_id or DEFAULT_LOCAL_MODEL
    if model_id not in LOCAL_MODELS:
        raise ValueError(f"Unknown local model '{model_id}'")

    url = f"{LOCAL_LLM_URL.rstrip('/')}/api/generate"
    response = requests.post(
        url,
        json={
            "model": model_id,
            "prompt": prompt,
            "stream": False,
        },
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()
    reply = data.get("response", "").strip()
    if not reply:
        raise RuntimeError("Local model returned an empty response")
    return reply


@app.route("/")
def home():
    app_config = {
        "modelOptions": MODEL_OPTIONS,
        "defaultProvider": DEFAULT_PROVIDER,
        "defaultModels": DEFAULT_MODELS,
        "localLLMEnabled": LOCAL_LLM_ENABLED,
        "groqEnabled": groq_client is not None,
    }
    return render_template("index.html", app_config=app_config)


@app.route("/chat", methods=["POST"])
def chat():
    payload = request.json or {}
    user_msg = payload.get("message", "").strip()
    language_code = (payload.get("language") or DEFAULT_LANGUAGE).lower()
    if language_code not in SUPPORTED_LANGUAGES:
        language_code = DEFAULT_LANGUAGE
    language_data = SUPPORTED_LANGUAGES[language_code]

    provider = (payload.get("provider") or DEFAULT_PROVIDER).lower()
    if provider not in MODEL_OPTIONS:
        provider = DEFAULT_PROVIDER

    if not user_msg:
        # Message for empty input always returned in English to keep tests deterministic
        return jsonify({
            "answer": "Please type something 🙂",
            "mode": "error",
            "language": language_code,
            "provider": provider,
        })

    reply = ""
    mode = "api"

    if provider == "local":
        if not LOCAL_LLM_ENABLED:
            reply = language_data["local_disabled_template"]
            mode = "local_disabled"
        else:
            try:
                model_id = payload.get("model") or DEFAULT_LOCAL_MODEL
                prompt = build_system_prompt(language_data, user_msg)
                reply = call_local_llm(prompt, model_id)
            except Exception as exc:  # broad catch to avoid breaking UI
                reply = language_data["local_error_template"].format(error=exc)
                mode = "local_error"
    elif provider == "groq":
        if not groq_client:
            reply = language_data["groq_disabled_template"]
            mode = "groq_disabled"
        else:
            try:
                model_name = payload.get("model") or DEFAULT_GROQ_MODEL
                resp = groq_client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": language_data["system_prompt"]},
                        {"role": "user", "content": user_msg}
                    ],
                    temperature=0.3,
                )
                reply = resp.choices[0].message.content
            except Exception as e:
                reply = language_data["api_error_template"].format(error=e)
                mode = "error"
    else:
        # Default to OpenAI provider
        if not openai_client:
            reply = language_data["offline_template"].format(message=user_msg)
            mode = "offline"
        else:
            try:
                model_name = payload.get("model") or DEFAULT_OPENAI_MODEL
                resp = openai_client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": language_data["system_prompt"]},
                        {"role": "user", "content": user_msg}
                    ],
                    temperature=0.3,
                )
                reply = resp.choices[0].message.content
            except Exception as e:
                reply = language_data["api_error_template"].format(error=e)
                mode = "error"

    # Store conversation in database
    try:
        conversation = Conversation(
            user_message=user_msg,
            bot_response=reply,
            session_id=payload.get("session_id", "default")
        )
        db.session.add(conversation)
        db.session.commit()
    except Exception as e:
        # Log error but don't break the response
        print(f"Database error: {e}")
        db.session.rollback()

    return jsonify({
        "answer": reply,
        "mode": mode,
        "language": language_code,
        "provider": provider,
    })


@app.route("/history", methods=["GET"])
def get_history():
    """Retrieve chat history"""
    session_id = request.args.get("session_id", "default")
    limit = request.args.get("limit", 50, type=int)
    
    try:
        conversations = Conversation.query.filter_by(
            session_id=session_id
        ).order_by(
            Conversation.created_at.desc()
        ).limit(limit).all()
        
        # Reverse to show oldest first
        conversations.reverse()
        
        return jsonify({
            "conversations": [conv.to_dict() for conv in conversations],
            "count": len(conversations)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/history/all", methods=["GET"])
def get_all_history():
    """Retrieve all chat history (across all sessions)"""
    limit = request.args.get("limit", 100, type=int)
    
    try:
        conversations = Conversation.query.order_by(
            Conversation.created_at.desc()
        ).limit(limit).all()
        
        conversations.reverse()
        
        return jsonify({
            "conversations": [conv.to_dict() for conv in conversations],
            "count": len(conversations)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/history/clear", methods=["POST"])
def clear_history():
    """Clear chat history for a session or all sessions"""
    session_id = request.json.get("session_id") if request.json else None
    
    try:
        if session_id:
            Conversation.query.filter_by(session_id=session_id).delete()
            message = f"History cleared for session: {session_id}"
        else:
            Conversation.query.delete()
            message = "All history cleared"
        
        db.session.commit()
        return jsonify({"message": message})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Development server only - use gunicorn for production
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    port = int(os.getenv("PORT", "5055"))
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    app.run(host=host, port=port, debug=debug_mode)


