from app.extensions import db
from datetime import datetime
import json

class Lead(db.Model):
    """Lead model representing users who submitted lead forms"""

    __tablename__ = 'leads'

    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    ad_id = db.Column(db.Integer, db.ForeignKey('ads.id'), nullable=False)
    user_fb_id = db.Column(db.String(100))
    user_name = db.Column(db.String(255))
    message_sent = db.Column(db.Boolean, default=False)
    message_text = db.Column(db.Text)
    message_sent_at = db.Column(db.DateTime)
    error_message = db.Column(db.Text)
    metadata = db.Column(db.Text, default='{}')  # JSON string for lead form data
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_metadata(self):
        """Get metadata as dictionary"""
        try:
            return json.loads(self.metadata) if self.metadata else {}
        except:
            return {}

    def set_metadata(self, metadata_dict):
        """Set metadata from dictionary"""
        self.metadata = json.dumps(metadata_dict)

    def to_dict(self):
        """Convert lead to dictionary"""
        return {
            'id': self.id,
            'lead_id': self.lead_id,
            'ad_id': self.ad_id,
            'user_fb_id': self.user_fb_id,
            'user_name': self.user_name,
            'message_sent': self.message_sent,
            'message_text': self.message_text,
            'message_sent_at': self.message_sent_at.isoformat() if self.message_sent_at else None,
            'error_message': self.error_message,
            'metadata': self.get_metadata(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Lead {self.lead_id}>'
