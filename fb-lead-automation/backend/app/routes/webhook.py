from flask import Blueprint, request, jsonify, current_app
import hmac
import hashlib

webhook_bp = Blueprint('webhook', __name__)


def verify_webhook_signature(payload, signature):
    """
    Проверяет подпись webhook от Facebook
    
    Args:
        payload: Тело запроса (bytes)
        signature: Подпись из заголовка X-Hub-Signature-256
    
    Returns:
        bool: True если подпись валидна
    """
    if not signature:
        current_app.logger.warning("No signature provided")
        return False
    
    # Получаем app_secret из конфига
    app_secret = current_app.config.get('FACEBOOK_APP_SECRET')
    if not app_secret:
        current_app.logger.error("FACEBOOK_APP_SECRET not configured")
        return False
    
    # Facebook отправляет подпись в формате: sha256=<hash>
    # Нужно убрать префикс "sha256="
    try:
        method, signature_hash = signature.split('=', 1)
    except ValueError:
        current_app.logger.warning(f"Invalid signature format: {signature}")
        return False
    
    if method != 'sha256':
        current_app.logger.warning(f"Unsupported signature method: {method}")
        return False
    
    # Вычисляем ожидаемую подпись
    expected_hash = hmac.new(
        app_secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    # Сравниваем подписи (используем hmac.compare_digest для защиты от timing attacks)
    is_valid = hmac.compare_digest(expected_hash, signature_hash)
    
    if not is_valid:
        current_app.logger.warning(
            f"Signature mismatch. Expected: {expected_hash[:10]}..., Got: {signature_hash[:10]}..."
        )
    
    return is_valid


@webhook_bp.route('/webhook', methods=['GET'])
def webhook_verify():
    """
    Верификация webhook (вызывается Facebook при настройке)
    """
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    verify_token = current_app.config.get('VERIFY_TOKEN')
    
    if mode == 'subscribe' and token == verify_token:
        current_app.logger.info("Webhook verified successfully")
        return challenge, 200
    else:
        current_app.logger.warning("Webhook verification failed")
        return 'Forbidden', 403


@webhook_bp.route('/webhook', methods=['POST'])
def webhook_event():
    """
    Обработка webhook событий от Facebook
    """
    # Получаем сырое тело запроса для проверки подписи
    payload = request.get_data()
    signature = request.headers.get('X-Hub-Signature-256')
    
    # ВАЖНО: В режиме разработки можно пропустить проверку подписи
    # Раскомментируйте следующие 2 строки для отладки:
    # if current_app.config.get('FLASK_ENV') == 'development':
    #     current_app.logger.info("Skipping signature verification in development mode")
    
    # Проверяем подпись (закомментируйте для отладки)
    if not verify_webhook_signature(payload, signature):
        current_app.logger.warning("Invalid webhook signature")
        return jsonify({'error': 'Invalid signature'}), 403
    
    # Парсим JSON
    try:
        data = request.get_json()
    except Exception as e:
        current_app.logger.error(f"Failed to parse webhook JSON: {e}")
        return jsonify({'error': 'Invalid JSON'}), 400
    
    current_app.logger.info(f"Received webhook: {data.get('object')}")
    
    # Обрабатываем события
    if data.get('object') == 'page':
        entries = data.get('entry', [])
        
        for entry in entries:
            changes = entry.get('changes', [])
            
            for change in changes:
                if change.get('field') == 'leadgen':
                    # Событие lead generation
                    leadgen_id = change.get('value', {}).get('leadgen_id')
                    ad_id = change.get('value', {}).get('ad_id')
                    form_id = change.get('value', {}).get('form_id')
                    
                    current_app.logger.info(
                        f"New lead: leadgen_id={leadgen_id}, ad_id={ad_id}, form_id={form_id}"
                    )
                    
                    # Обрабатываем лид в фоне (импортируем здесь чтобы избежать циклических импортов)
                    try:
                        from app.services.lead_processor import process_lead
                        process_lead(leadgen_id, ad_id, form_id)
                    except Exception as e:
                        current_app.logger.error(f"Error processing lead: {e}")
    
    # Всегда возвращаем 200 OK чтобы Facebook не повторял запрос
    return jsonify({'status': 'ok'}), 200


@webhook_bp.route('/webhook/test', methods=['POST'])
def webhook_test():
    """
    Тестовый endpoint без проверки подписи (только для разработки!)
    """
    if current_app.config.get('FLASK_ENV') != 'development':
        return jsonify({'error': 'Only available in development'}), 403
    
    data = request.get_json()
    current_app.logger.info(f"Test webhook received: {data}")
    
    # Обрабатываем как обычный webhook
    if data.get('object') == 'page':
        entries = data.get('entry', [])
        
        for entry in entries:
            changes = entry.get('changes', [])
            
            for change in changes:
                if change.get('field') == 'leadgen':
                    leadgen_id = change.get('value', {}).get('leadgen_id')
                    ad_id = change.get('value', {}).get('ad_id')
                    form_id = change.get('value', {}).get('form_id')
                    
                    current_app.logger.info(
                        f"Test lead: leadgen_id={leadgen_id}, ad_id={ad_id}"
                    )
                    
                    try:
                        from app.services.lead_processor import process_lead
                        process_lead(leadgen_id, ad_id, form_id)
                    except Exception as e:
                        current_app.logger.error(f"Error processing test lead: {e}")
    
    return jsonify({'status': 'ok', 'message': 'Test webhook processed'}), 200


