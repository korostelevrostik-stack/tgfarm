import asyncio
from flask import Flask
from threading import Thread
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN
from handlers import register_all_handlers
from database import init_db  # <-- ДОБАВЬ ЭТУ СТРОКУ

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

app = Flask(__name__)

@app.route('/')
def home():
    return "🚜 MEGA GARDEN 2.0 работает!"

@app.route('/health')
def health():
    return "OK", 200

async def main():
    print("🤖 MEGA GARDEN 2.0 запускается...")
    init_db()  # <-- ДОБАВЬ ЭТУ СТРОКУ (создаёт базу)
    register_all_handlers(dp)
    print("✅ Бот готов!")
    await dp.start_polling(bot)

def run_flask():
    app.run(host='0.0.0.0', port=10000, debug=False, use_reloader=False)

if __name__ == "__main__":
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("🌐 Веб-сервер запущен на порту 10000")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Бот остановлен")
