# handlers/plant.py
from aiogram import types
from handlers.start import players
from keyboards import main_menu

async def plant_menu(callback: types.CallbackQuery):
    """Показать меню посадки (вызывается из главного меню)"""
    user = players.get(callback.from_user.id)
    if not user:
        await callback.message.edit_text(
            "❌ Сначала напиши /start",
            reply_markup=main_menu()
        )
        await callback.answer()
        return
    
    # Проверяем, есть ли хоть что-то в crops
    has_crops = any(amount > 0 for amount in user.crops.values())
    
    if not has_crops:
        await callback.message.edit_text(
            f"🌱 У тебя нет семян!\n"
            f"💰 Денег: {user.money}$\n\n"
            f"Сначала купи семена в 🏪 Магазине!",
            reply_markup=main_menu()
        )
    else:
        # Показываем, что есть на складе
        crops_list = []
        for crop, amount in user.crops.items():
            if amount > 0:
                crops_list.append(f"{crop}: {amount} шт.")
        
        await callback.message.edit_text(
            f"🌱 У тебя есть семена:\n" + "\n".join(crops_list) + 
            f"\n\n💰 Денег: {user.money}$\n"
            f"Посадка происходит автоматически при покупке семян!",
            reply_markup=main_menu()
        )
    await callback.answer()

async def do_plant(callback: types.CallbackQuery):
    """Обработка покупки/посадки семян (вызывается из магазина)"""
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
    
    # Сажаем (покупаем семена и сразу сажаем)
    success, message = user.plant_crop(crop_name)
    
    # Возвращаемся в магазин
    from keyboards import shop_menu
    await callback.message.edit_text(
        message + "\n\n🏪 Вернуться в магазин",
        reply_markup=shop_menu()
    )
    await callback.answer()

def register_plant(dp):
    """Регистрация обработчиков"""
    dp.callback_query.register(plant_menu, lambda c: c.data == "plant")
    dp.callback_query.register(do_plant, lambda c: c.data.startswith("plant_"))
