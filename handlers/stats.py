# handlers/stats.py
from aiogram import types
from handlers.start import players
from keyboards import main_menu

async def stats_callback(callback: types.CallbackQuery):
    """Показать полную статистику фермы"""
    user = players.get(callback.from_user.id)
    if not user:
        await callback.message.edit_text(
            "❌ Сначала напиши /start",
            reply_markup=main_menu()
        )
        await callback.answer()
        return
    
    # Получаем статистику
    stats = user.get_stats()
    
    # Добавляем общую информацию
    total_crops = sum(user.crops.values())
    total_animals = sum(user.animals.values())
    
    stats += f"\n\n📊 Итого:"
    stats += f"\n🌾 Всего урожая: {total_crops} шт."
    stats += f"\n🐄 Всего животных: {total_animals} шт."
    
    await callback.message.edit_text(
        stats,
        reply_markup=main_menu()
    )
    await callback.answer()

def register_stats(dp):
    """Регистрация обработчиков"""
    dp.callback_query.register(stats_callback, lambda c: c.data == "stats")
