from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Ad
from app.services.facebook_service import FacebookService
from datetime import datetime

ads_bp = Blueprint('ads', __name__)

@ads_bp.route('', methods=['GET'])
def get_ads():
    """Get all ads with optional filtering"""
    try:
        is_active = request.args.get('is_active')

        query = Ad.query

        if is_active is not None:
            is_active_bool = is_active.lower() in ['true', '1', 'yes']
            query = query.filter_by(is_active=is_active_bool)

        ads = query.order_by(Ad.created_at.desc()).all()

        return jsonify({
            'success': True,
            'data': [ad.to_dict() for ad in ads],
            'count': len(ads)
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ads_bp.route('/<int:ad_id>', methods=['GET'])
def get_ad(ad_id):
    """Get specific ad by ID"""
    try:
        ad = Ad.query.get_or_404(ad_id)

        return jsonify({
            'success': True,
            'data': ad.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404


@ads_bp.route('/sync', methods=['POST'])
def sync_ads():
    """Manually trigger ad synchronization with Facebook"""
    try:
        facebook_service = FacebookService()
        ads_data = facebook_service.get_active_ads()

        if not ads_data:
            return jsonify({
                'success': False,
                'error': 'Failed to fetch ads from Facebook. Check your credentials.'
            }), 500

        # Get all existing ad IDs
        existing_ad_ids = {ad.ad_id for ad in Ad.query.all()}
        synced_ad_ids = set()

        # Upsert ads
        synced_count = 0
        created_count = 0

        for ad_data in ads_data:
            ad_id = ad_data.get('id')
            synced_ad_ids.add(ad_id)

            ad = Ad.query.filter_by(ad_id=ad_id).first()

            if ad:
                # Update existing ad
                ad.ad_name = ad_data.get('name', ad.ad_name)
                ad.status = ad_data.get('status', ad.status)
                ad.is_active = True
                ad.last_synced_at = datetime.utcnow()
                synced_count += 1
            else:
                # Create new ad
                ad = Ad(
                    ad_id=ad_id,
                    ad_name=ad_data.get('name', ''),
                    campaign_id=ad_data.get('campaign', {}).get('id'),
                    campaign_name=ad_data.get('campaign', {}).get('name'),
                    adset_id=ad_data.get('adset', {}).get('id'),
                    adset_name=ad_data.get('adset', {}).get('name'),
                    status=ad_data.get('status'),
                    is_active=True,
                    last_synced_at=datetime.utcnow()
                )
                db.session.add(ad)
                created_count += 1

        # Mark missing ads as inactive
        missing_ad_ids = existing_ad_ids - synced_ad_ids
        deactivated_count = 0

        for ad_id in missing_ad_ids:
            ad = Ad.query.filter_by(ad_id=ad_id).first()
            if ad and ad.is_active:
                ad.is_active = False
                deactivated_count += 1

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Ads synchronized successfully',
            'stats': {
                'total': len(ads_data),
                'created': created_count,
                'updated': synced_count,
                'deactivated': deactivated_count
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ads_bp.route('/<int:ad_id>', methods=['DELETE'])
def delete_ad(ad_id):
    """Delete ad from database"""
    try:
        ad = Ad.query.get_or_404(ad_id)
        db.session.delete(ad)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Ad deleted successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
