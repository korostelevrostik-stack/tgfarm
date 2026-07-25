# handlers/levels.py
from aiogram import types
from aiogram.filters import Command
from handlers.start import players

async def level_up(user):
    """Повысить уровень фермера"""
    if not hasattr(user, 'exp'):
        user.exp = 0
        user.level = 1
    
    # За каждую продажу даём опыт
    user.exp += 1
    
    # Проверяем, не пора ли повысить уровень
    exp_needed = user.level * 10  # 10, 20, 30, ...
    if user.exp >= exp_needed:
        user.level += 1
        user.exp = 0
        return True
    return False

async def profile_command(message: types.Message):
    user = players.get(message.from_user.id)
    if not user:
        await message.answer("❌ /start")
        return
    
    if not hasattr(user, 'level'):
        user.level = 1
        user.exp = 0
    
    exp_needed = user.level * 10
    await message.answer(
        f"👨‍🌾 **Профиль фермера**\n\n"
        f"📊 Уровень: {user.level}\n"
        f"⭐ Опыт: {user.exp}/{exp_needed}\n"
        f"💰 Денег: {user.money}$\n"
        f"📅 Дней: {user.day}"
    )

def register_levels(dp):
    dp.message.register(profile_command, Command("profile"))
