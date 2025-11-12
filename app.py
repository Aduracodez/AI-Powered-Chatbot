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
    user_msg = (request.json or {}).get("message", "").strip()
    session_id = (request.json or {}).get("session_id", "default")
    
    if not user_msg:
        return jsonify({"answer": "Please type something 🙂"})

    reply = ""
    
    # Offline fallback so the page works even without a key
    if not openai_client:
        reply = f"(offline demo) You said: {user_msg}"
    else:
        # OpenAI path (simple, low-cost model)
        try:
            resp = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a friendly, concise chatbot."},
                    {"role": "user", "content": user_msg}
                ],
                temperature=0.3,
            )
            reply = resp.choices[0].message.content
        except Exception as e:
            # Never break the UI if API fails
            reply = f"(API error) {e}"
    
    # Store conversation in database
    try:
        conversation = Conversation(
            user_message=user_msg,
            bot_response=reply,
            session_id=session_id
        )
        db.session.add(conversation)
        db.session.commit()
    except Exception as e:
        # Log error but don't break the response
        print(f"Database error: {e}")
        db.session.rollback()
    
    return jsonify({"answer": reply})


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
    # Explicit host/port to avoid confusion
    app.run(host="127.0.0.1", port=5000, debug=True)


