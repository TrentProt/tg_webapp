import logging.config

from backend.config import CONFIG


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] [{levelname}] [{name}] [{module}:{lineno}] [{funcName}] {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{asctime}] [{levelname}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'simple',
        },
        'app_file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'INFO',
            'formatter': 'verbose',
            'filename': str(CONFIG.LOG_DIR / 'app.log'),
            'when': 'midnight',
            'backupCount': 7,
            'delay': True,
        },
        'error_file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'verbose',
            'filename': str(CONFIG.LOG_DIR / 'errors.log'),
            'when': 'midnight',
            'backupCount': 7,
            'delay': True,
        },
    },
    'root': {
        'handlers': ['console', 'app_file', 'error_file'],
        'level': 'INFO',
    },
    'loggers': {
        'uvicorn': {
            'handlers': ['console', 'app_file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'uvicorn.access': {
            'handlers': ['console', 'app_file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'uvicorn.error': {
            'handlers': ['console', 'app_file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'gunicorn.access': {
            'handlers': ['console', 'app_file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'gunicorn.error': {
            'handlers': ['console', 'app_file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'watchfiles.main': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}


def setup_logging() -> None:
    """Глобальная настройка логов. Применяется один раз при сборке приложения."""

    # Обработчики консоли и файла логов.
    CONFIG.LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.config.dictConfig(LOGGING_CONFIG)

    if CONFIG.logging.debug_mode:
        LOGGING_CONFIG['handlers']['console']['level'] = 'DEBUG'
        LOGGING_CONFIG['loggers']['src'] = {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        }

    logging.config.dictConfig(LOGGING_CONFIG)
