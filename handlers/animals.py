# handlers/animals.py
from aiogram import types
from handlers.start import players
from keyboards import main_menu, animal_menu

async def animal_menu_callback(callback: types.CallbackQuery):
    """Показать меню покупки животных"""
    await callback.message.edit_text(
        "🐾 Кого покупаем?\n\n"
        "Выбери животное:",
        reply_markup=animal_menu()
    )
    await callback.answer()

async def buy_animal_callback(callback: types.CallbackQuery):
    """Обработка покупки животного"""
    user = players.get(callback.from_user.id)
    if not user:
        await callback.message.edit_text(
            "❌ Сначала напиши /start",
            reply_markup=main_menu()
        )
        await callback.answer()
        return
    
    # Получаем название животного из callback_data
    animal_name = callback.data.replace("buy_", "")
    
    # Покупаем
    success, message = user.buy_animal(animal_name)
    
    await callback.message.edit_text(
        message,
        reply_markup=main_menu()
    )
    await callback.answer()

async def collect_products_callback(callback: types.CallbackQuery):
    """Собрать продукцию животных"""
    user = players.get(callback.from_user.id)
    if not user:
        await callback.message.edit_text(
            "❌ Сначала напиши /start",
            reply_markup=main_menu()
        )
        await callback.answer()
        return
    
    # Собираем продукцию
    total_earn, message = user.collect_products()
    
    # Добавляем итог, если что-то собрали
    if total_earn > 0:
        message += f"\n\n💰 Итого: +{total_earn}$"
    else:
        message += "\n\n🐄 Купи животных и приходи завтра!"
    
    await callback.message.edit_text(
        message,
        reply_markup=main_menu()
    )
    await callback.answer()

def register_animals(dp):
    """Регистрация обработчиков"""
    dp.callback_query.register(animal_menu_callback, lambda c: c.data == "buy_animal")
    dp.callback_query.register(buy_animal_callback, lambda c: c.data.startswith("buy_"))
    dp.callback_query.register(collect_products_callback, lambda c: c.data == "animal_products")
