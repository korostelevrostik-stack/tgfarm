import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN
from handlers import register_all_handlers

# Создаём бота и диспетчер с хранилищем для FSM
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

async def main():
    print("🤖 MEGA GARDEN 2.0 запускается...")
    register_all_handlers(dp)
    print("✅ Бот готов!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
