# handlers/admin.py
from aiogram import types
from aiogram.filters import Command
from config import ADMIN_ID
from handlers.start import players
from models import START_MONEY

async def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID

async def admin_panel(message: types.Message):
    if not await is_admin(message.from_user.id):
        await message.answer("⛔ Нет прав!")
        return
    
    total_players = len(players)
    total_money = sum(p.money for p in players.values())
    
    await message.answer(
        f"👑 **Админ-панель**\n\n"
        f"👤 Игроков: {total_players}\n"
        f"💰 Всего денег: {total_money}$\n\n"
        f"📋 Команды:\n"
        f"/giveall 100 — дать всем денег\n"
        f"/resetall — сбросить всех\n"
        f"/players — список игроков",
        parse_mode="Markdown"
    )

async def give_all_money(message: types.Message):
    if not await is_admin(message.from_user.id):
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 2:
            await message.answer("❌ Использование: /giveall сумма")
            return
        
        amount = int(parts[1])
        
        if not players:
            await message.answer("😴 Нет игроков")
            return
        
        for player in players.values():
            player.money += amount
        
        await message.answer(f"✅ Выдал {amount}$ всем {len(players)} игрокам!")
        
    except ValueError:
        await message.answer("❌ Сумма должна быть числом!")

async def reset_all_players(message: types.Message):
    if not await is_admin(message.from_user.id):
        return
    
    if not players:
        await message.answer("😴 Нет игроков")
        return
    
    for player in players.values():
        player.money = START_MONEY
        player.crops = {crop: 0 for crop in player.crops.keys()}
        player.animals = {animal: 0 for animal in player.animals.keys()}
        player.day = 1
    
    await message.answer(f"✅ Сбросил {len(players)} игроков!")

async def list_players(message: types.Message):
    if not await is_admin(message.from_user.id):
        return
    
    if not players:
        await message.answer("😴 Нет игроков")
        return
    
    text = "👤 **Список игроков:**\n\n"
    for i, (user_id, player) in enumerate(players.items(), 1):
        text += f"{i}. ID: `{user_id}` | 💰 {player.money}$ | 📅 День {player.day}\n"
    
    await message.answer(text, parse_mode="Markdown")

def register_admin(dp):
    dp.message.register(admin_panel, Command("admin"))
    dp.message.register(give_all_money, Command("giveall"))
    dp.message.register(reset_all_players, Command("resetall"))
    dp.message.register(list_players, Command("players"))
