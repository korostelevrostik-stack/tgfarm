# handlers/harvest.py
from aiogram import types
from handlers.start import players
from keyboards import main_menu

async def harvest_callback(callback: types.CallbackQuery):
    """Собрать урожай"""
    user = players.get(callback.from_user.id)
    if not user:
        await callback.message.edit_text(
            "❌ Сначала напиши /start",
            reply_markup=main_menu()
        )
        await callback.answer()
        return
    
    # Собираем урожай
    total_earn, message = user.harvest_all()
    
    # Добавляем итог, если что-то собрали
    if total_earn > 0:
        message += f"\n\n💰 Итого: +{total_earn}$"
    else:
        message += "\n\n🌱 Посади что-нибудь и приходи завтра!"
    
    await callback.message.edit_text(
        message,
        reply_markup=main_menu()
    )
    await callback.answer()

def register_harvest(dp):
    """Регистрация обработчиков"""
    dp.callback_query.register(harvest_callback, lambda c: c.data == "harvest")
