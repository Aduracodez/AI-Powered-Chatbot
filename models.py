from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Conversation(db.Model):
    """Model to store chat conversations"""
    __tablename__ = 'conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    session_id = db.Column(db.String(100), nullable=True)  # Optional: for multi-session support
    
    def to_dict(self):
        """Convert conversation to dictionary for JSON response"""
        return {
            'id': self.id,
            'user_message': self.user_message,
            'bot_response': self.bot_response,
            'created_at': self.created_at.isoformat(),
            'session_id': self.session_id
        }
    
    def __repr__(self):
        return f'<Conversation {self.id}: {self.user_message[:50]}...>'

