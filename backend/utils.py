import hmac
import hashlib
import logging
from urllib.parse import unquote

logger = logging.getLogger(__name__)


def validate_init_data(init_data: str, bot_token: str) -> bool:
    """
    Проверяет initData от Telegram WebApp.
    Возвращает True если данные валидны.
    """
    try:
        # Парсим параметры
        params = {}
        for pair in init_data.split('&'):
            if '=' in pair:
                key, value = pair.split('=', 1)
                params[key] = value

        logger.info(f"Все параметры: {list(params.keys())}")
        logger.info(f"bot_token начинается с: {bot_token[:15]}...")

        # Извлекаем хэш
        hash_received = params.pop('hash', '')
        if not hash_received:
            logger.error("Хэш не найден в параметрах!")
            return False

        logger.info(f"Полученный хэш: {hash_received}")
        logger.info(f"Параметры без hash: {params}")

        # Создаем строку для проверки
        check_string = '\n'.join(
            f"{k}={unquote(v)}"
            for k, v in sorted(params.items())
        )

        logger.info(f"Строка для проверки:\n{check_string}")

        # Создаем ключ: HMAC(bot_token, "WebAppData")
        secret_key = hmac.new(
            key=b"WebAppData",
            msg=bot_token.encode(),
            digestmod=hashlib.sha256
        ).digest()

        # Вычисляем хэш
        calculated_hash = hmac.new(
            key=secret_key,
            msg=check_string.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        logger.info(f"Вычисленный хэш: {calculated_hash}")
        logger.info(f"Сравниваем: '{hash_received}' == '{calculated_hash}'")

        # Ccравнение
        result = hmac.compare_digest(calculated_hash, hash_received)
        logger.info(f"Результат валидации: {result}")
        logger.info("=" * 50)

        return result

    except Exception as e:
        logger.error(f"ОШИБКА при проверке: {str(e)}", exc_info=True)
        return False
