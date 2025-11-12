import pytest
import os
from unittest.mock import patch, MagicMock
from app import app


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
        assert 'answer' in data
        assert 'Please type something' in data['answer']
    
    def test_chat_route_with_empty_string(self, client):
        """Test chat route with empty string message."""
        response = client.post('/chat',
                             json={'message': '   '},
                             content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert 'Please type something' in data['answer']
    
    @patch.dict(os.environ, {}, clear=True)
    @patch('app.openai_client', None)
    def test_chat_route_offline_mode(self, client):
        """Test chat route in offline mode (no OpenAI key)."""
        response = client.post('/chat',
                             json={'message': 'Hello'},
                             content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert 'answer' in data
        assert 'offline demo' in data['answer'].lower()
        assert 'Hello' in data['answer']
    
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
                             json={'message': 'Hello'},
                             content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert 'answer' in data
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
        assert 'answer' in data
        assert 'api error' in data['answer'].lower()
    
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

