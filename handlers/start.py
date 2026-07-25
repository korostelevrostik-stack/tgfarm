# handlers/start.py
from aiogram import types
from aiogram.filters import Command
from models import Player
from keyboards import main_menu, shop_menu

players = {}

async def start_command(message: types.Message):
    """Команда /start"""
    user_id = message.from_user.id
    if user_id not in players:
        players[user_id] = Player(user_id)
    
    await message.answer(
        f"🚜 Привет, {message.from_user.first_name}!\n"
        f"💰 {players[user_id].money}$ | 📅 День {players[user_id].day}\n\n"
        f"Выбирай действие:",
        reply_markup=main_menu()
    )

async def back_callback(callback: types.CallbackQuery):
    """Назад в главное меню"""
    user = players.get(callback.from_user.id)
    if user:
        await callback.message.edit_text(
            f"🚜 Главное меню\n💰 {user.money}$ | 📅 День {user.day}",
            reply_markup=main_menu()
        )
    await callback.answer()

async def shop_callback(callback: types.CallbackQuery):
    """Открыть магазин"""
    user = players.get(callback.from_user.id)
    if user:
        await callback.message.edit_text(
            f"🏪 Магазин\n💰 {user.money}$\n\nВыбери, что купить:",
            reply_markup=shop_menu()
        )
    await callback.answer()

async def back_shop_callback(callback: types.CallbackQuery):
    """Назад в магазин"""
    user = players.get(callback.from_user.id)
    if user:
        await callback.message.edit_text(
            f"🏪 Магазин\n💰 {user.money}$\n\nВыбери, что купить:",
            reply_markup=shop_menu()
        )
    await callback.answer()

async def buy_seeds_callback(callback: types.CallbackQuery):
    """Открыть меню семян"""
    from keyboards import seeds_menu
    user = players.get(callback.from_user.id)
    if user:
        await callback.message.edit_text(
            f"🌾 Выбери семена:\n💰 {user.money}$",
            reply_markup=seeds_menu()
        )
    await callback.answer()

async def buy_animals_shop_callback(callback: types.CallbackQuery):
    """Открыть меню животных в магазине"""
    from keyboards import animals_shop_menu
    user = players.get(callback.from_user.id)
    if user:
        await callback.message.edit_text(
            f"🐄 Выбери животное:\n💰 {user.money}$",
            reply_markup=animals_shop_menu()
        )
    await callback.answer()

def register_start(dp):
    dp.message.register(start_command, Command("start"))
    dp.callback_query.register(back_callback, lambda c: c.data == "back")
    dp.callback_query.register(shop_callback, lambda c: c.data == "shop")
    dp.callback_query.register(back_shop_callback, lambda c: c.data == "back_shop")
    dp.callback_query.register(buy_seeds_callback, lambda c: c.data == "buy_seeds")
    dp.callback_query.register(buy_animals_shop_callback, lambda c: c.data == "buy_animals")
