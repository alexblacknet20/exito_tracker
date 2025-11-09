import requests
from flask import current_app

class MessengerService:
    """Service for sending messages via Facebook Messenger API"""

    def __init__(self):
        self.page_access_token = current_app.config.get('PAGE_ACCESS_TOKEN')
        self.base_url = 'https://graph.facebook.com/v18.0/me/messages'

    def send_message(self, recipient_id, message_text):
        """
        Send a message to a user via Messenger

        Args:
            recipient_id: Facebook user ID
            message_text: Message text to send

        Returns:
            bool: True if message sent successfully, False otherwise
        """
        try:
            if not self.page_access_token:
                current_app.logger.warning('Page access token not configured')
                return False

            if not recipient_id or not message_text:
                current_app.logger.error('Recipient ID and message text are required')
                return False

            payload = {
                'recipient': {
                    'id': recipient_id
                },
                'message': {
                    'text': message_text
                }
            }

            params = {
                'access_token': self.page_access_token
            }

            response = requests.post(
                self.base_url,
                params=params,
                json=payload
            )

            response.raise_for_status()

            result = response.json()
            message_id = result.get('message_id')

            if message_id:
                current_app.logger.info(f'Message sent successfully to {recipient_id} (message_id: {message_id})')
                return True
            else:
                current_app.logger.warning(f'No message_id in response: {result}')
                return False

        except requests.exceptions.RequestException as e:
            current_app.logger.error(f'Messenger API error: {str(e)}')
            if hasattr(e, 'response') and e.response is not None:
                current_app.logger.error(f'Response: {e.response.text}')
            return False
        except Exception as e:
            current_app.logger.error(f'Error sending message: {str(e)}')
            return False
