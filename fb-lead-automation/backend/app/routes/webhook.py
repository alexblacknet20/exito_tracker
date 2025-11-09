from flask import Blueprint, request, jsonify, current_app
from app.extensions import db
from app.models import Lead, Ad, MessageTemplate
from app.services.facebook_service import FacebookService
from app.services.messenger_service import MessengerService
from app.services.template_service import TemplateService
from datetime import datetime
import hmac
import hashlib

webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('', methods=['GET'])
def verify_webhook():
    """Verify webhook for Facebook"""
    try:
        # Get query parameters
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        # Verify token
        if mode == 'subscribe' and token == current_app.config['VERIFY_TOKEN']:
            current_app.logger.info('Webhook verified successfully')
            return challenge, 200
        else:
            current_app.logger.warning('Webhook verification failed')
            return 'Forbidden', 403

    except Exception as e:
        current_app.logger.error(f'Webhook verification error: {str(e)}')
        return 'Error', 500


@webhook_bp.route('', methods=['POST'])
def handle_webhook():
    """Handle incoming leadgen events from Facebook"""
    try:
        # Verify signature
        signature = request.headers.get('X-Hub-Signature-256', '')
        if not verify_signature(request.data, signature):
            current_app.logger.warning('Invalid webhook signature')
            return 'Forbidden', 403

        data = request.get_json()
        current_app.logger.info(f'Received webhook: {data}')

        # Process each entry
        for entry in data.get('entry', []):
            for change in entry.get('changes', []):
                if change.get('field') == 'leadgen':
                    process_leadgen_event(change.get('value', {}))

        return 'OK', 200

    except Exception as e:
        current_app.logger.error(f'Webhook handling error: {str(e)}')
        return 'Error', 500


def verify_signature(payload, signature):
    """Verify webhook signature using HMAC-SHA256"""
    try:
        app_secret = current_app.config['FACEBOOK_APP_SECRET']
        if not app_secret:
            return True  # Skip verification if no secret configured

        expected_signature = 'sha256=' + hmac.new(
            app_secret.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected_signature, signature)

    except Exception as e:
        current_app.logger.error(f'Signature verification error: {str(e)}')
        return False


def process_leadgen_event(event_data):
    """Process a leadgen event"""
    try:
        leadgen_id = event_data.get('leadgen_id')
        ad_id = event_data.get('ad_id')
        form_id = event_data.get('form_id')
        page_id = event_data.get('page_id')

        current_app.logger.info(f'Processing lead: {leadgen_id} for ad: {ad_id}')

        # Check for duplicate lead
        existing_lead = Lead.query.filter_by(lead_id=leadgen_id).first()
        if existing_lead:
            current_app.logger.info(f'Lead {leadgen_id} already processed')
            return

        # Find ad in database
        ad = Ad.query.filter_by(ad_id=ad_id).first()
        if not ad:
            current_app.logger.warning(f'Ad {ad_id} not found in database')
            # Create a placeholder lead without sending message
            lead = Lead(
                lead_id=leadgen_id,
                ad_id=None,
                error_message='Ad not found in database'
            )
            db.session.add(lead)
            db.session.commit()
            return

        # Fetch lead data from Facebook
        facebook_service = FacebookService()
        lead_data = facebook_service.get_lead_data(leadgen_id)

        if not lead_data:
            current_app.logger.error(f'Failed to fetch lead data for {leadgen_id}')
            lead = Lead(
                lead_id=leadgen_id,
                ad_id=ad.id,
                error_message='Failed to fetch lead data from Facebook'
            )
            db.session.add(lead)
            db.session.commit()
            return

        # Extract user information
        user_fb_id = lead_data.get('id')
        field_data = {item['name']: item['values'][0] for item in lead_data.get('field_data', [])}

        user_name = field_data.get('full_name') or f"{field_data.get('first_name', '')} {field_data.get('last_name', '')}".strip()

        # Find message template for this ad
        template = MessageTemplate.query.filter_by(ad_id=ad.id, is_active=True).first()

        if not template:
            current_app.logger.warning(f'No active template found for ad {ad_id}')
            lead = Lead(
                lead_id=leadgen_id,
                ad_id=ad.id,
                user_fb_id=user_fb_id,
                user_name=user_name,
                error_message='No active message template found'
            )
            lead.set_metadata(field_data)
            db.session.add(lead)
            db.session.commit()
            return

        # Fill template with lead data
        template_service = TemplateService()
        message_text = template_service.fill_template(
            template.message_text,
            field_data,
            template.get_variables()
        )

        # Send message via Messenger
        messenger_service = MessengerService()
        success = messenger_service.send_message(user_fb_id, message_text)

        # Save lead to database
        lead = Lead(
            lead_id=leadgen_id,
            ad_id=ad.id,
            user_fb_id=user_fb_id,
            user_name=user_name,
            message_sent=success,
            message_text=message_text,
            message_sent_at=datetime.utcnow() if success else None,
            error_message=None if success else 'Failed to send message via Messenger'
        )
        lead.set_metadata(field_data)
        db.session.add(lead)
        db.session.commit()

        current_app.logger.info(f'Lead {leadgen_id} processed successfully. Message sent: {success}')

    except Exception as e:
        current_app.logger.error(f'Error processing leadgen event: {str(e)}')
        db.session.rollback()
