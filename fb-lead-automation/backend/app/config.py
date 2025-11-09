import os
from datetime import timedelta

class Config:
    """Application configuration class"""

    # Secret key for session management
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Facebook API configuration
    FACEBOOK_APP_ID = os.getenv('FACEBOOK_APP_ID', '')
    FACEBOOK_APP_SECRET = os.getenv('FACEBOOK_APP_SECRET', '')
    FACEBOOK_ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN', '')
    FACEBOOK_AD_ACCOUNT_ID = os.getenv('FACEBOOK_AD_ACCOUNT_ID', '')

    # Messenger API configuration
    PAGE_ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN', '')

    # Webhook configuration
    VERIFY_TOKEN = os.getenv('VERIFY_TOKEN', 'my_webhook_token')

    # Scheduler configuration
    AD_SYNC_INTERVAL_MINUTES = int(os.getenv('AD_SYNC_INTERVAL_MINUTES', '10'))
    SCHEDULER_API_ENABLED = True

    # CORS configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
