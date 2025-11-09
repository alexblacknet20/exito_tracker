import requests
import json
from flask import current_app


class FacebookService:
    """Service for interacting with Facebook Marketing API"""

    def __init__(self):
        self.access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")
        self.ad_account_id = current_app.config.get("FACEBOOK_AD_ACCOUNT_ID")
        self.base_url = "https://graph.facebook.com/v24.0"

    def get_active_ads(self):
        """
        Fetch active ads from Facebook Marketing API

        Returns:
            list: List of ad dictionaries or None on error
        """
        try:
            if not self.access_token or not self.ad_account_id:
                current_app.logger.warning("Facebook credentials not configured")
                return None

            url = f"{self.base_url}/act_{self.ad_account_id}/ads"

            params = {
                "access_token": self.access_token,
                "fields": "id,name,status,campaign{id,name},adset{id,name}",
                # ИСПРАВЛЕНИЕ: преобразуем массив в JSON строку
                # Facebook API требует формат: effective_status=["ACTIVE","PAUSED"]
                "effective_status": json.dumps(["ACTIVE", "PAUSED"]),
                "limit": 100,
            }

            all_ads = []
            next_url = url

            # Handle pagination
            while next_url:
                response = requests.get(
                    next_url, params=params if next_url == url else None
                )
                response.raise_for_status()

                data = response.json()
                ads = data.get("data", [])
                all_ads.extend(ads)

                # Get next page URL
                paging = data.get("paging", {})
                next_url = paging.get("next")
                params = None  # Clear params for subsequent requests

                current_app.logger.info(
                    f"Fetched {len(ads)} ads (total: {len(all_ads)})"
                )

                # Safety limit to prevent infinite loops
                if len(all_ads) >= 1000:
                    current_app.logger.warning("Reached ad limit of 1000")
                    break

            current_app.logger.info(
                f"Successfully fetched {len(all_ads)} ads from Facebook"
            )
            return all_ads

        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Facebook API error: {str(e)}")
            if hasattr(e, "response") and e.response is not None:
                current_app.logger.error(f"Response: {e.response.text}")
            return None
        except Exception as e:
            current_app.logger.error(f"Error fetching ads: {str(e)}")
            return None

    def get_lead_data(self, leadgen_id):
        """
        Fetch specific lead data from Facebook

        Args:
            leadgen_id: Facebook lead ID

        Returns:
            dict: Lead data or None on error
        """
        try:
            if not self.access_token:
                current_app.logger.warning("Facebook access token not configured")
                return None

            url = f"{self.base_url}/{leadgen_id}"

            params = {
                "access_token": self.access_token,
                "fields": "id,created_time,field_data",
            }

            response = requests.get(url, params=params)
            response.raise_for_status()

            lead_data = response.json()
            current_app.logger.info(f"Successfully fetched lead data for {leadgen_id}")
            return lead_data

        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Facebook API error fetching lead: {str(e)}")
            if hasattr(e, "response") and e.response is not None:
                current_app.logger.error(f"Response: {e.response.text}")
            return None
        except Exception as e:
            current_app.logger.error(f"Error fetching lead data: {str(e)}")
            return None