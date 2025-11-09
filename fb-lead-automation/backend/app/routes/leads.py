from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Lead, Ad
from sqlalchemy import func

leads_bp = Blueprint('leads', __name__)

@leads_bp.route('', methods=['GET'])
def get_leads():
    """Get all leads with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)

        # Limit per_page to avoid performance issues
        per_page = min(per_page, 100)

        pagination = Lead.query.order_by(Lead.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        # Enrich leads with ad information
        leads_data = []
        for lead in pagination.items:
            lead_dict = lead.to_dict()
            if lead.ad:
                lead_dict['ad_name'] = lead.ad.ad_name
            leads_data.append(lead_dict)

        return jsonify({
            'success': True,
            'data': leads_data,
            'pagination': {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@leads_bp.route('/<int:lead_id>', methods=['GET'])
def get_lead(lead_id):
    """Get specific lead by ID"""
    try:
        lead = Lead.query.get_or_404(lead_id)

        lead_dict = lead.to_dict()
        if lead.ad:
            lead_dict['ad_name'] = lead.ad.ad_name
            lead_dict['campaign_name'] = lead.ad.campaign_name

        return jsonify({
            'success': True,
            'data': lead_dict
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404


@leads_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get lead statistics"""
    try:
        total_leads = Lead.query.count()
        messages_sent = Lead.query.filter_by(message_sent=True).count()
        messages_failed = Lead.query.filter(
            Lead.message_sent == False,
            Lead.error_message.isnot(None)
        ).count()

        # Calculate success rate
        success_rate = 0
        if total_leads > 0:
            success_rate = round((messages_sent / total_leads) * 100, 2)

        # Get leads by ad
        leads_by_ad = db.session.query(
            Ad.ad_name,
            func.count(Lead.id).label('count')
        ).join(Lead).group_by(Ad.id).all()

        return jsonify({
            'success': True,
            'data': {
                'total_leads': total_leads,
                'messages_sent': messages_sent,
                'messages_failed': messages_failed,
                'success_rate': success_rate,
                'leads_by_ad': [
                    {'ad_name': ad_name, 'count': count}
                    for ad_name, count in leads_by_ad
                ]
            }
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
