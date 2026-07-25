# handlers/day.py
from aiogram import types
from handlers.start import players
from keyboards import main_menu

async def next_day_callback(callback: types.CallbackQuery):
    """Переход на следующий день"""
    user = players.get(callback.from_user.id)
    if not user:
        await callback.message.edit_text(
            "❌ Сначала напиши /start",
            reply_markup=main_menu()
        )
        await callback.answer()
        return
    
    # Переходим на следующий день
    message = user.next_day()
    
    # Добавляем статистику
    message += f"\n\n💰 Денег: {user.money}$"
    message += f"\n🌾 Урожай: {sum(user.crops.values())} шт."
    message += f"\n🐄 Животных: {sum(user.animals.values())} шт."
    
    await callback.message.edit_text(
        message,
        reply_markup=main_menu()
    )
    await callback.answer()

def register_day(dp):
    """Регистрация обработчиков"""
    dp.callback_query.register(next_day_callback, lambda c: c.data == "next_day")
