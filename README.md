# 🤖 AI-Powered Chatbot

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Framework-lightgrey.svg)](https://flask.palletsprojects.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-success.svg)](https://platform.openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Made with ❤️ by Aduracodez](https://img.shields.io/badge/Made%20with%20%E2%9D%A4%EF%B8%8F-by%20Aduracodez-red)](https://github.com/Aduracodez)

An intelligent, conversational chatbot built with **Python**, **Flask**, and **OpenAI GPT models**.  
Designed to deliver natural conversations, answer FAQs, or serve as a foundation for your own AI assistant.

---

## 🧠 Features

- 💬 **Natural conversation** powered by OpenAI GPT models  
- ⚡ **Lightweight Flask backend** — easy to run locally or deploy anywhere  
- 🧩 **Offline fallback mode** (echoes user input if no API key is set)  
- 🪶 **Simple web UI** built with HTML, CSS, and JavaScript  
- 🔐 **Secure API key management** via environment variables  
- 🧰 **Extensible design** — easily integrate FAQs, memory, or FastAPI  

---

## 🏗️ Project Structure

AI-Powered-Chatbot/
├── app.py / main.py # Flask or FastAPI backend
├── templates/
│ └── index.html # Chat UI
├── static/
│ └── main.js # Frontend logic
├── data/
│ └── faqs.json # (optional) FAQ data
├── requirements.txt # Dependencies
└── README.md # Documentation

---

## ⚙️ Installation

### 1️⃣ Clone the repository
```bash
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
🔑 Setup OpenAI API Key
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
Modify system behavior
{"role": "system", "content": "You are a friendly support assistant."}
Add FAQs or contextual data
Edit data/faqs.json
Integrate it into your chatbot logic for smarter responses
🚀 Deployment
Deploy easily on:
Render
Railway
Vercel (with FastAPI)
PythonAnywhere
All platforms require:
Your repository
The environment variable OPENAI_API_KEY
💡 Future Enhancements
🧠 Persistent memory for multi-turn conversations
🪄 FAQ integration via RAG (Retrieval-Augmented Generation)
🎙️ Voice mode (Speech-to-Text + Text-to-Speech)
🧾 Admin dashboard for managing FAQs
📜 License
Licensed under the MIT License — free to use, modify, and distribute.
👨‍💻 Author
@Aduracodez
Building smart, accessible AI tools for everyone. 💡
🌟 If you like this project, don’t forget to star ⭐ the repo!


