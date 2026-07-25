# handlers/plant.py
from aiogram import types
from handlers.start import players
from keyboards import main_menu, crop_menu

async def plant_menu(callback: types.CallbackQuery):
    """Показать меню выбора культур"""
    await callback.message.edit_text(
        "🌱 Что сажаем?\n\n"
        "Выбери культуру:",
        reply_markup=crop_menu()
    )
    await callback.answer()

async def do_plant(callback: types.CallbackQuery):
    """Обработка посадки культуры"""
    user = players.get(callback.from_user.id)
    if not user:
        await callback.message.edit_text(
            "❌ Сначала напиши /start",
            reply_markup=main_menu()
        )
        await callback.answer()
        return
    
    # Получаем название культуры из callback_data
    crop_name = callback.data.replace("plant_", "")
    
    # Сажаем
    success, message = user.plant_crop(crop_name)
    
    await callback.message.edit_text(
        message,
        reply_markup=main_menu()
    )
    await callback.answer()

def register_plant(dp):
    """Регистрация обработчиков"""
    dp.callback_query.register(plant_menu, lambda c: c.data == "plant")
    dp.callback_query.register(do_plant, lambda c: c.data.startswith("plant_"))
