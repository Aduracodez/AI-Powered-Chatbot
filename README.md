🤖 AI-Powered Chatbot
An intelligent, conversational chatbot built with Python, Flask, and OpenAI GPT models.
Designed to deliver natural conversations, answer FAQs, or serve as a foundation for your own AI assistant.
🧠 Key Features
💬 Natural conversation powered by OpenAI GPT models
⚡ Lightweight Flask backend — easy to run locally or deploy anywhere
🧩 Offline fallback mode (echoes user input when no API key is set)
🪶 Clean, simple web UI built with HTML, CSS, and JavaScript
🔐 Secure API key management via environment variables
🧰 Extensible design — add FAQ logic, memory, FastAPI, or more with minimal effort
🏗️ Project Structure
AI-Powered-Chatbot/
├── app.py / main.py       # Flask or FastAPI backend
├── templates/
│   └── index.html         # Chat interface
├── static/
│   └── main.js            # Frontend logic
├── data/
│   └── faqs.json          # (optional) FAQ data
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
⚙️ Installation
1️⃣ Clone the repository
git clone https://github.com/Aduracodez/AI-Powered-Chatbot.git
cd AI-Powered-Chatbot
2️⃣ Create and activate a virtual environment
Windows
python -m venv venv
venv\Scripts\activate
macOS / Linux
python -m venv venv
source venv/bin/activate
3️⃣ Install dependencies
pip install -r requirements.txt
🔑 OpenAI API Setup
This chatbot uses the OpenAI API for generating responses.
Option 1 – Temporary (per session)
macOS / Linux
export OPENAI_API_KEY=sk-your-key
Windows PowerShell
$env:OPENAI_API_KEY="sk-your-key"
Option 2 – Persistent (.env file)
Create a .env file in the project root:
OPENAI_API_KEY=sk-your-key
MODEL_NAME=gpt-4o-mini
Then load it in your Python file:
from dotenv import load_dotenv
load_dotenv()
▶️ Run the App
Flask version
python app.py
FastAPI version
python main.py
Then open your browser to:
👉 http://127.0.0.1:5050/
🧪 Example Chat
User: Hello there!
Bot: Hi! 👋 How can I help you today?
🛠️ Customization
Change the default model
model = "gpt-4o-mini"  # or "gpt-3.5-turbo"
Modify the system behavior
{"role": "system", "content": "You are a friendly support assistant."}
Add FAQs or contextual data
Edit data/faqs.json
Integrate it into your chatbot logic for smarter responses
🚀 Deployment
You can easily deploy on:
Render
Railway
Vercel (with FastAPI)
PythonAnywhere
All platforms only require:
Your repository
OPENAI_API_KEY as an environment variable
📜 License
This project is licensed under the MIT License.
Feel free to fork, modify, and build on top of it.
💡 Future Enhancements
🧠 Persistent memory for multi-turn conversations
🪄 FAQ integration with RAG (Retrieval-Augmented Generation)
🎙️ Voice mode (Speech-to-Text + Text-to-Speech)
🧾 Admin panel for FAQ and chat management
👨‍💻 Author
@Aduracodez
Building smart, accessible AI tools for everyone. 💡
