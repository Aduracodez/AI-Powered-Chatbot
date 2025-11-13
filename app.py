from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from models import db, Conversation

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
    },
}
DEFAULT_LANGUAGE = "en"

# Only use OpenAI if a key is present (so the UI still works without a key) 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = None
if OPENAI_API_KEY:
    try:
        from openai import OpenAI
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
    except Exception:
        openai_client = None  # fall back gracefully

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    payload = request.json or {}
    user_msg = payload.get("message", "").strip()
    language_code = (payload.get("language") or DEFAULT_LANGUAGE).lower()
    if language_code not in SUPPORTED_LANGUAGES:
        language_code = DEFAULT_LANGUAGE
    language_data = SUPPORTED_LANGUAGES[language_code]

    if not user_msg:
        # Message for empty input always returned in English to keep tests deterministic
        return jsonify({
            "answer": "Please type something 🙂",
            "mode": "error",
            "language": language_code,
        })

    reply = ""
    mode = "api"

    if not openai_client:
        reply = language_data["offline_template"].format(message=user_msg)
        mode = "offline"
    else:
        try:
            resp = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
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
    app.run(host="127.0.0.1", port=5000, debug=debug_mode)


