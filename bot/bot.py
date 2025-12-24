import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from backend.config import CONFIG


bot = Bot(CONFIG.tgbot.api_key)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(msg: types.Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="Открыть каталог",
                web_app=types.WebAppInfo(url=CONFIG.tgbot.web_url),
            )]
        ]
    )
    await msg.answer("Каталог контейнеров:", reply_markup=kb)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
