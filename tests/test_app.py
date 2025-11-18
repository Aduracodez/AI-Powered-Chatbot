import pytest
import os
from unittest.mock import patch, MagicMock
from app import app, DEFAULT_LOCAL_MODEL, DEFAULT_OPENAI_MODEL, DEFAULT_GROQ_MODEL


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHomeRoute:
    """Test cases for the home route."""
    
    def test_home_route_returns_200(self, client):
        """Test that the home route returns a 200 status code."""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_home_route_returns_html(self, client):
        """Test that the home route returns HTML content."""
        response = client.get('/')
        assert 'text/html' in response.content_type
        assert b'AI Powered Chatbot' in response.data


class TestChatRoute:
    """Test cases for the chat route."""
    
    def test_chat_route_without_message(self, client):
        """Test chat route with empty message."""
        response = client.post('/chat', 
                             json={},
                             content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['mode'] == 'error'
        assert data['language'] == 'en'
        assert data['provider'] == 'openai'
        assert 'Please type something' in data['answer']
    
    def test_chat_route_with_empty_string(self, client):
        """Test chat route with empty string message."""
        response = client.post('/chat',
                             json={'message': '   '},
                             content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['mode'] == 'error'
        assert data['provider'] == 'openai'
        assert 'Please type something' in data['answer']
    
    @patch.dict(os.environ, {}, clear=True)
    @patch('app.openai_client', None)
    def test_chat_route_offline_mode(self, client):
        """Test chat route in offline mode (no OpenAI key)."""
        response = client.post('/chat',
                             json={'message': 'Hallo', 'language': 'de'},
                             content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['mode'] == 'offline'
        assert data['language'] == 'de'
        assert data['provider'] == 'openai'
        assert 'Offline-Demo' in data['answer']
        assert 'Hallo' in data['answer']
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    @patch('app.openai_client')
    def test_chat_route_with_openai_success(self, mock_client, client):
        """Test chat route with successful OpenAI response."""
        # Mock OpenAI response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Hello! How can I help you?"
        mock_client.chat.completions.create.return_value = mock_response
        
        response = client.post('/chat',
                             json={'message': 'Hello', 'model': DEFAULT_OPENAI_MODEL},
                             content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['mode'] == 'api'
        assert data['language'] == 'en'
        assert data['provider'] == 'openai'
        assert data['answer'] == "Hello! How can I help you?"
        mock_client.chat.completions.create.assert_called_once()
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    @patch('app.openai_client')
    def test_chat_route_with_openai_error(self, mock_client, client):
        """Test chat route handles OpenAI API errors gracefully."""
        # Mock OpenAI to raise an exception
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        
        response = client.post('/chat',
                             json={'message': 'Hello'},
                             content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['mode'] == 'error'
        assert data['language'] == 'en'
        assert data['provider'] == 'openai'
        assert 'api error' in data['answer'].lower()
    
    @patch('app.LOCAL_LLM_ENABLED', False)
    def test_chat_route_local_disabled(self, client):
        """Ensure helpful message when local provider selected but disabled."""
        response = client.post('/chat',
                             json={'message': 'Hallo', 'provider': 'local', 'language': 'de', 'model': DEFAULT_LOCAL_MODEL},
                             content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['mode'] == 'local_disabled'
        assert data['provider'] == 'local'
        assert 'Lokales Modell' in data['answer']
    
    @patch('app.LOCAL_LLM_ENABLED', True)
    @patch('app.call_local_llm')
    def test_chat_route_local_success(self, mock_local_llm, client):
        """Test chat route with local LLM provider."""
        mock_local_llm.return_value = "Hallo! Wie kann ich helfen?"
        response = client.post('/chat',
                             json={'message': 'Hallo', 'provider': 'local', 'model': DEFAULT_LOCAL_MODEL, 'language': 'de'},
                             content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['mode'] == 'api'
        assert data['provider'] == 'local'
        assert 'Hallo!' in data['answer']
        mock_local_llm.assert_called_once()

    @patch('app.groq_client', None)
    def test_chat_route_groq_disabled(self, client):
        """Ensure helpful message when Groq selected without API key."""
        response = client.post('/chat',
                             json={'message': 'Hello', 'provider': 'groq', 'language': 'en', 'model': DEFAULT_GROQ_MODEL},
                             content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['mode'] == 'groq_disabled'
        assert data['provider'] == 'groq'
        assert 'Groq' in data['answer']

    @patch('app.groq_client')
    def test_chat_route_groq_success(self, mock_groq_client, client):
        """Test chat route with Groq provider."""
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_choice.message.content = "Groq says hallo!"
        mock_response.choices = [mock_choice]
        mock_groq_client.chat.completions.create.return_value = mock_response

        response = client.post('/chat',
                             json={'message': 'Hello', 'provider': 'groq', 'model': DEFAULT_GROQ_MODEL},
                             content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['provider'] == 'groq'
        assert data['mode'] == 'api'
        assert 'Groq says hallo' in data['answer']
        mock_groq_client.chat.completions.create.assert_called_once()
    
    def test_chat_route_invalid_json(self, client):
        """Test chat route with invalid JSON."""
        response = client.post('/chat',
                             data='invalid json',
                             content_type='application/json')
        # Flask returns 400 for invalid JSON
        assert response.status_code == 400


class TestAppInitialization:
    """Test cases for app initialization."""
    
    def test_app_exists(self):
        """Test that the Flask app instance exists."""
        assert app is not None
    
    def test_app_is_flask_instance(self):
        """Test that app is a Flask instance."""
        from flask import Flask
        assert isinstance(app, Flask)

