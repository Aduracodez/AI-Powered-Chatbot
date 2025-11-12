from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")

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
    if not user_msg:
        return jsonify({"answer": "Please type something 🙂"})

    # Offline fallback so the page works even without a key
    if not openai_client:
        return jsonify({"answer": f"(offline demo) You said: {user_msg}"})

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
        return jsonify({"answer": reply})
    except Exception as e:
        # Never break the UI if API fails
        return jsonify({"answer": f"(API error) {e}"}), 200

if __name__ == "__main__":
    # Explicit host/port to avoid confusion
    app.run(host="127.0.0.1", port=5050, debug=True)


