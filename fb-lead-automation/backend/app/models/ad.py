from app.extensions import db
from datetime import datetime

class Ad(db.Model):
    """Ad model representing Facebook/Instagram ads"""

    __tablename__ = 'ads'

    id = db.Column(db.Integer, primary_key=True)
    ad_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    ad_name = db.Column(db.String(255), nullable=False)
    campaign_id = db.Column(db.String(100))
    campaign_name = db.Column(db.String(255))
    adset_id = db.Column(db.String(100))
    adset_name = db.Column(db.String(255))
    status = db.Column(db.String(50))
    platform = db.Column(db.String(50), default='facebook')
    is_active = db.Column(db.Boolean, default=True)
    last_synced_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    message_template = db.relationship('MessageTemplate', backref='ad', uselist=False, cascade='all, delete-orphan')
    leads = db.relationship('Lead', backref='ad', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        """Convert ad to dictionary"""
        return {
            'id': self.id,
            'ad_id': self.ad_id,
            'ad_name': self.ad_name,
            'campaign_id': self.campaign_id,
            'campaign_name': self.campaign_name,
            'adset_id': self.adset_id,
            'adset_name': self.adset_name,
            'status': self.status,
            'platform': self.platform,
            'is_active': self.is_active,
            'last_synced_at': self.last_synced_at.isoformat() if self.last_synced_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'has_template': self.message_template is not None
        }

    def __repr__(self):
        return f'<Ad {self.ad_name}>'
