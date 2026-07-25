from aiogram import types
from aiogram.filters import Command
from models import Player
from keyboards import main_menu, shop_menu, seeds_menu, animals_shop_menu

players = {}

async def start_command(message: types.Message):
    user_id = message.from_user.id
    if user_id not in players:
        players[user_id] = Player(user_id)
    
    await message.answer(
        f"🚜 Привет, {message.from_user.first_name}!\n"
        f"💰 {players[user_id].money}$ | 📅 День {players[user_id].day}\n\n"
        f"🌾 Начинай с Пшеницы! Продавай урожай, чтобы разблокировать новые культуры.",
        reply_markup=main_menu()
    )

async def back_callback(callback: types.CallbackQuery):
    user = players.get(callback.from_user.id)
    if user:
        await callback.message.edit_text(
            f"🚜 Главное меню\n💰 {user.money}$ | 📅 День {user.day}",
            reply_markup=main_menu()
        )
    await callback.answer()

async def shop_callback(callback: types.CallbackQuery):
    user = players.get(callback.from_user.id)
    if user:
        await callback.message.edit_text(
            f"🏪 Магазин\n💰 {user.money}$\n\nВыбери, что купить:",
            reply_markup=shop_menu()
        )
    await callback.answer()

async def back_shop_callback(callback: types.CallbackQuery):
    user = players.get(callback.from_user.id)
    if user:
        await callback.message.edit_text(
            f"🏪 Магазин\n💰 {user.money}$\n\nВыбери, что купить:",
            reply_markup=shop_menu()
        )
    await callback.answer()

async def buy_seeds_callback(callback: types.CallbackQuery):
    user = players.get(callback.from_user.id)
    if user:
        await callback.message.edit_text(
            f"🌾 Выбери семена:\n💰 {user.money}$\n\n"
            f"🔓 Разблокировано: {len(user.unlocked_crops)} из {len(CROP_DATA)}",
            reply_markup=seeds_menu(user)
        )
    await callback.answer()

async def buy_animals_shop_callback(callback: types.CallbackQuery):
    user = players.get(callback.from_user.id)
    if user:
        await callback.message.edit_text(
            f"🐄 Выбери животное:\n💰 {user.money}$",
            reply_markup=animals_shop_menu()
        )
    await callback.answer()

async def plant_command(message: types.Message):
    user = players.get(message.from_user.id)
    if not user:
        await message.answer("❌ Напиши /start")
        return
    
    await message.answer(
        f"🌱 Твои семена:\n" + "\n".join([f"{crop}: {amount}шт" for crop, amount in user.crops.items() if amount > 0]) or "Пусто",
        reply_markup=main_menu()
    )

async def harvest_command(message: types.Message):
    user = players.get(message.from_user.id)
    if not user:
        await message.answer("❌ Напиши /start")
        return
    
    total_earn, msg = user.harvest_all()
    await message.answer(msg, reply_markup=main_menu())

async def shop_command(message: types.Message):
    user = players.get(message.from_user.id)
    if not user:
        await message.answer("❌ Напиши /start")
        return
    
    await message.answer(
        f"🏪 Магазин\n💰 {user.money}$\n\nВыбери, что купить:",
        reply_markup=shop_menu()
    )

async def products_command(message: types.Message):
    user = players.get(message.from_user.id)
    if not user:
        await message.answer("❌ Напиши /start")
        return
    
    total_earn, msg = user.collect_products()
    await message.answer(msg, reply_markup=main_menu())

def register_start(dp):
    dp.message.register(start_command, Command("start"))
    dp.message.register(plant_command, Command("plant"))
    dp.message.register(harvest_command, Command("harvest"))
    dp.message.register(shop_command, Command("shop"))
    dp.message.register(products_command, Command("products"))
    
    dp.callback_query.register(back_callback, lambda c: c.data == "back")
    dp.callback_query.register(shop_callback, lambda c: c.data == "shop")
    dp.callback_query.register(back_shop_callback, lambda c: c.data == "back_shop")
    dp.callback_query.register(buy_seeds_callback, lambda c: c.data == "buy_seeds")
    dp.callback_query.register(buy_animals_shop_callback, lambda c: c.data == "buy_animals")
