import asyncio
from flask import Flask
from threading import Thread
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN
from handlers import register_all_handlers

# ========== НАСТРОЙКА БОТА ==========
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# ========== FLASK СЕРВЕР ДЛЯ RENDER ==========
app = Flask(__name__)

@app.route('/')
def home():
    return "🚜 MEGA GARDEN 2.0 работает!"

@app.route('/health')
def health():
    return "OK", 200

# ========== ЗАПУСК БОТА ==========
async def main():
    """Главная асинхронная функция"""
    print("🤖 MEGA GARDEN 2.0 запускается...")
    register_all_handlers(dp)
    print("✅ Бот готов!")
    
    # Запускаем поллинг
    await dp.start_polling(bot)

def run_flask():
    """Запуск Flask в отдельном потоке"""
    app.run(host='0.0.0.0', port=10000, debug=False, use_reloader=False)

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    # Запускаем Flask в отдельном потоке
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("🌐 Веб-сервер запущен на порту 10000")
    
    # Запускаем бота в основном потоке (асинхронно)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Бот остановлен")
