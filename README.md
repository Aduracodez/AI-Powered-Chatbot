# AI Powered Chatbot

A Flask-based chatbot application with OpenAI integration.

## Features

- 🤖 AI-powered chat using OpenAI GPT-3.5-turbo
- 🔄 Offline fallback mode (works without API key)
- 🎨 Modern, clean UI
- ✅ Comprehensive test coverage
- 🚀 CI/CD pipeline with GitHub Actions

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
```

6. Run the application:
```bash
python app.py
```

The app will be available at `http://127.0.0.1:5050`

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
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
├── pytest.ini             # Pytest configuration
├── .flake8                 # Flake8 configuration
└── pyproject.toml          # Black, isort, coverage config
```

## License

MIT

