from app.extensions import db
from datetime import datetime
import json

class MessageTemplate(db.Model):
    """Message template model for personalized messages"""

    __tablename__ = 'message_templates'

    id = db.Column(db.Integer, primary_key=True)
    ad_id = db.Column(db.Integer, db.ForeignKey('ads.id'), unique=True, nullable=False)
    template_name = db.Column(db.String(255), nullable=False)
    message_text = db.Column(db.Text, nullable=False)
    variables = db.Column(db.Text, default='{}')  # JSON string for custom variables
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_variables(self):
        """Get variables as dictionary"""
        try:
            return json.loads(self.variables) if self.variables else {}
        except:
            return {}

    def set_variables(self, variables_dict):
        """Set variables from dictionary"""
        self.variables = json.dumps(variables_dict)

    def to_dict(self):
        """Convert message template to dictionary"""
        return {
            'id': self.id,
            'ad_id': self.ad_id,
            'template_name': self.template_name,
            'message_text': self.message_text,
            'variables': self.get_variables(),
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<MessageTemplate {self.template_name}>'
