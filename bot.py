import asyncio
import threading
from flask import Flask
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

def run_bot():
    """Запуск бота в отдельном потоке"""
    asyncio.run(dp.start_polling(bot))

def run_flask():
    """Запуск Flask сервера для Render"""
    app.run(host='0.0.0.0', port=10000)

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("🤖 MEGA GARDEN 2.0 запускается...")
    register_all_handlers(dp)
    print("✅ Бот готов!")
    
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    
    # Запускаем Flask в основном потоке (для Render)
    print("🌐 Запускаю веб-сервер на порту 10000...")
    run_flask()
