import time
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
from backend.config import CONFIG

client = TelegramClient(
    'sessions/session',
    int(CONFIG.tguser.api_id),
    CONFIG.tguser.api_hash
)

last_reply = {}

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if not event.is_private:
        return

    sender = await event.get_sender()
    if sender is None or sender.bot:
        return

    text = event.text.strip()
    now = time.time()

    if text == 'приветAPP':
        if now - last_reply.get(sender.id, 0) < 10:
            return
        try:
            await event.reply(CONFIG.tgbot.web_url)
            last_reply[sender.id] = now
            print(f'Ответ отправлен {sender.id}')
        except FloodWaitError as e:
            print(f'FloodWait {e.seconds}s')

async def main():
    await client.start()
    print('User client started')
    await client.run_until_disconnected()

import asyncio
asyncio.run(main())

