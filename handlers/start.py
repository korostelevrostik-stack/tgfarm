# handlers/start.py
from aiogram import types
from aiogram.filters import Command
from models import Player
from keyboards import main_menu

# Временное хранилище игроков (потом заменим на БД)
players = {}

async def start_command(message: types.Message):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    
    # Создаём нового игрока, если его нет
    if user_id not in players:
        players[user_id] = Player(user_id)
    
    await message.answer(
        f"🚜 Привет, {message.from_user.first_name}!\n"
        f"Добро пожаловать на ферму!\n\n"
        f"💰 У тебя {players[user_id].money}$\n"
        f"📅 День {players[user_id].day}\n\n"
        f"Выбирай действие в меню ниже:",
        reply_markup=main_menu()
    )

async def back_callback(callback: types.CallbackQuery):
    """Кнопка 'Назад' — возвращает в главное меню"""
    await callback.message.edit_text(
        "🚜 Главное меню",
        reply_markup=main_menu()
    )
    await callback.answer()

def register_start(dp):
    """Регистрация обработчиков"""
    dp.message.register(start_command, Command("start"))
    dp.callback_query.register(back_callback, lambda c: c.data == "back")
