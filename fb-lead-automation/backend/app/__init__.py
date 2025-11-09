from flask import Flask
from app.config import Config
from app.extensions import db, migrate, cors, scheduler
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})

    # Register blueprints
    from app.routes.ads import ads_bp
    from app.routes.messages import messages_bp
    from app.routes.leads import leads_bp
    from app.routes.webhook import webhook_bp

    app.register_blueprint(ads_bp, url_prefix='/api/ads')
    app.register_blueprint(messages_bp, url_prefix='/api/messages')
    app.register_blueprint(leads_bp, url_prefix='/api/leads')
    app.register_blueprint(webhook_bp, url_prefix='/api/webhook')

    # Initialize scheduler
    if not scheduler.running:
        from app.jobs.ad_sync_job import schedule_ad_sync
        schedule_ad_sync(app)
        scheduler.start()

    # Create tables
    with app.app_context():
        db.create_all()

    return app
