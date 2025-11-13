# AI Powered Chatbot

A Flask-based chatbot application with OpenAI integration.

## Features

- 🤖 AI-powered chat using OpenAI GPT-3.5-turbo
- 💾 Database integration with SQLite/PostgreSQL for chat history
- 🔄 Offline fallback mode (works without API key)
- 🎨 Modern, clean UI
- ✅ Comprehensive test coverage
- 🚀 CI/CD pipeline with GitHub Actions
- 📦 Production-ready with gunicorn

## Setup

### Prerequisites

- Python 3.10 or higher
- pip

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd AI_Power_Chatbot
```

2. Create and activate a virtual environment:
```bash
python -m venv mychatbot
source mychatbot/bin/activate  # On Windows: mychatbot\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

5. Create a `.env` file in the root directory:
```bash
OPENAI_API_KEY=your-api-key-here
# Optional: For PostgreSQL in production
# DATABASE_URL=postgresql://user:password@host:port/dbname
```

6. Run the application:
```bash
python app.py
```

The app will be available at `http://127.0.0.1:5000`

**Note:** The database (SQLite by default) will be created automatically on first run.

## Development

### Running Tests

```bash
pytest
```

With coverage:
```bash
pytest --cov=. --cov-report=html
```

### Code Quality

Format code with black:
```bash
black .
```

Check code style with flake8:
```bash
flake8 .
```

Sort imports with isort:
```bash
isort .
```

### Security Checks

Run safety check:
```bash
safety check
```

Run bandit security linter:
```bash
bandit -r .
```

## Deployment

For production deployment, see [DEPLOYMENT.md](DEPLOYMENT.md) for detailed guides on:

- 🚂 Railway
- 🎨 Render
- 🟣 Heroku
- ☁️ AWS Elastic Beanstalk
- 🐳 Docker
- And more!

**Quick start with Railway (easiest):**
1. Push code to GitHub
2. Connect repo to [railway.app](https://railway.app)
3. Add environment variables
4. Deploy! ✨

## API Endpoints

- `POST /chat` - Send a message to the chatbot
- `GET /history` - Get chat history for a session
- `GET /history/all` - Get all chat history
- `POST /history/clear` - Clear chat history

## CI/CD Pipeline

The project includes a GitHub Actions CI/CD pipeline that:

- ✅ Runs tests on Python 3.10, 3.11, and 3.12
- ✅ Checks code quality (flake8, black)
- ✅ Runs security scans (safety, bandit)
- ✅ Generates test coverage reports
- ✅ Builds artifacts on main branch pushes

The pipeline runs automatically on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

## Project Structure

```
AI_Power_Chatbot/
├── .github/
│   └── workflows/
│       └── ci.yml          # CI/CD pipeline
├── static/
│   └── main.js             # Frontend JavaScript
├── templates/
│   └── index.html          # Main HTML template
├── tests/
│   ├── __init__.py
│   └── test_app.py         # Test suite
├── app.py                  # Main Flask application
├── models.py               # Database models
├── wsgi.py                 # WSGI entry point for production
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
├── Procfile                # For Heroku/Railway deployment
├── Dockerfile              # Docker configuration
├── DEPLOYMENT.md           # Deployment guide
├── pytest.ini             # Pytest configuration
├── .flake8                 # Flake8 configuration
└── pyproject.toml          # Black, isort, coverage config
```

## License

MIT

