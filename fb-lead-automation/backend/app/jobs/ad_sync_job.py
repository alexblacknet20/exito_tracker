from app.extensions import db, scheduler
from app.models import Ad
from app.services.facebook_service import FacebookService
from datetime import datetime

def sync_ads_job(app):
    """
    Background job to sync ads from Facebook Marketing API
    Runs periodically to keep local database in sync
    """
    with app.app_context():
        try:
            app.logger.info('Starting ad sync job...')

            facebook_service = FacebookService()
            ads_data = facebook_service.get_active_ads()

            if not ads_data:
                app.logger.warning('No ads fetched from Facebook')
                return

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

            # Mark missing ads as inactive (don't delete)
            missing_ad_ids = existing_ad_ids - synced_ad_ids
            deactivated_count = 0

            for ad_id in missing_ad_ids:
                ad = Ad.query.filter_by(ad_id=ad_id).first()
                if ad and ad.is_active:
                    ad.is_active = False
                    deactivated_count += 1

            db.session.commit()

            app.logger.info(
                f'Ad sync completed: {created_count} created, '
                f'{synced_count} updated, {deactivated_count} deactivated'
            )

        except Exception as e:
            app.logger.error(f'Error in ad sync job: {str(e)}')
            db.session.rollback()


def schedule_ad_sync(app):
    """
    Schedule the ad sync job to run periodically

    Args:
        app: Flask application instance
    """
    interval_minutes = app.config.get('AD_SYNC_INTERVAL_MINUTES', 10)

    scheduler.add_job(
        id='sync_ads',
        func=sync_ads_job,
        args=[app],
        trigger='interval',
        minutes=interval_minutes,
        replace_existing=True
    )

    app.logger.info(f'Ad sync job scheduled to run every {interval_minutes} minutes')
