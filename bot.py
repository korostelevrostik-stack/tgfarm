# bot.py
import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import register_all_handlers

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    print("🤖 Ферма-бот запускается...")
    register_all_handlers(dp)
    print("✅ Бот готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
