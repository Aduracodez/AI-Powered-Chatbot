🤖 AI-Powered Chatbot
An intelligent, conversational chatbot built with Python and OpenAI GPT models, using a simple Flask web interface.
It can answer FAQs, hold casual conversations, or serve as a starting point for any AI assistant.
🧠 Features
💬 Natural, friendly conversation powered by OpenAI GPT
⚡ Lightweight Flask backend (easy to run locally or deploy)
🧩 Offline fallback mode (echoes user input when no API key)
🪶 Simple web UI built with HTML, CSS, and JavaScript
🔐 Secure — API key stored as an environment variable
🧰 Ready for extension (FAQ knowledge base, FastAPI, memory, etc.)
🏗️ Project Structure
AI-Powered-Chatbot/
├── app.py / main.py          # Flask or FastAPI server
├── templates/
│   └── index.html            # Chat UI
├── static/
│   └── main.js               # Frontend logic
├── data/
│   └── faqs.json             # (optional) FAQ data for Smart mode
├── requirements.txt          # Python dependencies
└── README.md                 # This file
⚙️ Installation
1️⃣ Clone the repository
git clone https://github.com/Aduracodez/AI-Powered-Chatbot.git
cd AI-Powered-Chatbot
2️⃣ Create a virtual environment
python -m venv venv
# Activate it:
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
3️⃣ Install dependencies
pip install -r requirements.txt
🔑 Setup OpenAI API Key
This project uses the OpenAI API for responses.
Option 1: Temporary (per session)
# macOS / Linux
export OPENAI_API_KEY=sk-your-key
# Windows PowerShell
$env:OPENAI_API_KEY="sk-your-key"
Option 2: Persistent via .env
Create a .env file in the project root:
OPENAI_API_KEY=sk-your-key
MODEL_NAME=gpt-4o-mini
Then add this line near the top of your Python file:
from dotenv import load_dotenv
load_dotenv()
▶️ Run the App
Flask version:
python app.py
FastAPI version (if using main.py):
python main.py
Then open your browser to:
http://127.0.0.1:5050/
🧪 Example Chat
User:
Hello there!
Bot:
Hi! 👋 How can I help you today?
🛠️ Customization
To change the default model → edit:
model="gpt-4o-mini"   # or "gpt-3.5-turbo"
To modify system behavior → adjust the system prompt:
{"role": "system", "content": "You are a friendly support assistant."}
To add FAQs or context → edit data/faqs.json and integrate them into the chat logic.
🚀 Deployment
You can deploy easily on:
Render.com
Railway.app
Vercel (with FastAPI)
PythonAnywhere
Each service just needs your repo + the environment variable OPENAI_API_KEY.
📜 License
This project is open-source under the MIT License.
Feel free to fork, modify, and build on top of it.
💡 Future Improvements
🧠 Add memory for multi-turn conversation
🪄 Integrate FAQ / RAG (retrieval augmented generation)
🎙️ Add voice chat (Speech-to-Text + Text-to-Speech)
🧾 Add an admin panel to manage FAQs
👨‍💻 Author
@Aduracodez
Building smart, accessible AI tools for everyone.
