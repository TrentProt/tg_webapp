# TgWebApp Project

Проект состоит из трёх основных компонентов:

1. **Backend** — FastAPI, отдаёт каталог контейнеров. 
2. **Bot** — Telegram Bot, кнопка открывает WebApp.  
3. **User Client** — Telegram User API клиент, отвечает на сообщение "приветAPP" ссылкой на WebApp.

---

## Структура проекта

```bash
tgapp/
├── backend/
│ ├── main.py
│ ├── config.py
│ ├── data.py
│ └── ...
├── bot/
│ └── bot.py
├── user_client/
│ ├── client.py
│ └── sessions/
├── webapp/
│ └── static/
│ ├── index.html
│ ├── item.html
│ └── app.js
├── requirements.txt
├── docker-compose.yml
├── .env.example
├── Dockerfile
└── .env
```

## Настройки
Создайте файл `.env` на основе `.env.example` и заполните переменные:

```env
# Logging
LOGGING_DEBUG_MODE=TRUE

# FastAPI
FASTAPI_PORT=8000
FASTAPI_HOST=0.0.0.0

# Telegram Bot
TGBOT_API_KEY=<ваш токен бота>
TGBOT_WEB_URL=<публичный URL WebApp>

# Telegram User
TGUSER_API_HASH=<ваш api_hash>
TGUSER_API_ID=<ваш api_id>
```

Для работы User API клиента нужна сессия.
Сначала запустите локально:

```bash
python -m user_client.client
```

## Запуск через Docker Compose
Поднимаем все сервисы (backend, бот, User API клиент):
```bash
docker compose up --build -d
```