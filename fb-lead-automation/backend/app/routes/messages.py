from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import MessageTemplate, Ad
from app.services.template_service import TemplateService

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('', methods=['GET'])
def get_messages():
    """Get all message templates"""
    try:
        templates = MessageTemplate.query.order_by(MessageTemplate.created_at.desc()).all()

        return jsonify({
            'success': True,
            'data': [template.to_dict() for template in templates],
            'count': len(templates)
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@messages_bp.route('/<int:template_id>', methods=['GET'])
def get_message(template_id):
    """Get specific message template"""
    try:
        template = MessageTemplate.query.get_or_404(template_id)

        return jsonify({
            'success': True,
            'data': template.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404


@messages_bp.route('', methods=['POST'])
def create_message():
    """Create new message template"""
    try:
        data = request.get_json()

        # Validate required fields
        if not data.get('ad_id'):
            return jsonify({
                'success': False,
                'error': 'ad_id is required'
            }), 400

        if not data.get('template_name'):
            return jsonify({
                'success': False,
                'error': 'template_name is required'
            }), 400

        if not data.get('message_text'):
            return jsonify({
                'success': False,
                'error': 'message_text is required'
            }), 400

        # Check if ad exists
        ad = Ad.query.get(data['ad_id'])
        if not ad:
            return jsonify({
                'success': False,
                'error': 'Ad not found'
            }), 404

        # Check if template already exists for this ad
        existing_template = MessageTemplate.query.filter_by(ad_id=data['ad_id']).first()
        if existing_template:
            return jsonify({
                'success': False,
                'error': 'Template already exists for this ad. Use PUT to update.'
            }), 409

        # Create template
        template = MessageTemplate(
            ad_id=data['ad_id'],
            template_name=data['template_name'],
            message_text=data['message_text'],
            is_active=data.get('is_active', True)
        )

        # Set variables if provided
        if 'variables' in data:
            template.set_variables(data['variables'])

        db.session.add(template)
        db.session.commit()

        return jsonify({
            'success': True,
            'data': template.to_dict(),
            'message': 'Template created successfully'
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@messages_bp.route('/<int:template_id>', methods=['PUT'])
def update_message(template_id):
    """Update existing message template"""
    try:
        template = MessageTemplate.query.get_or_404(template_id)
        data = request.get_json()

        # Update fields
        if 'template_name' in data:
            template.template_name = data['template_name']

        if 'message_text' in data:
            template.message_text = data['message_text']

        if 'variables' in data:
            template.set_variables(data['variables'])

        if 'is_active' in data:
            template.is_active = data['is_active']

        db.session.commit()

        return jsonify({
            'success': True,
            'data': template.to_dict(),
            'message': 'Template updated successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@messages_bp.route('/<int:template_id>', methods=['DELETE'])
def delete_message(template_id):
    """Delete message template"""
    try:
        template = MessageTemplate.query.get_or_404(template_id)
        db.session.delete(template)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Template deleted successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@messages_bp.route('/<int:template_id>/preview', methods=['POST'])
def preview_message(template_id):
    """Preview template with sample data"""
    try:
        template = MessageTemplate.query.get_or_404(template_id)
        data = request.get_json() or {}

        # Get sample lead data
        sample_lead_data = data.get('lead_data', {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '+1234567890'
        })

        # Fill template
        template_service = TemplateService()
        filled_message = template_service.fill_template(
            template.message_text,
            sample_lead_data,
            template.get_variables()
        )

        return jsonify({
            'success': True,
            'data': {
                'original': template.message_text,
                'preview': filled_message,
                'placeholders': template_service.extract_placeholders(template.message_text)
            }
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
