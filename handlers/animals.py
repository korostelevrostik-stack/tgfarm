# handlers/animals.py
from aiogram import types
from handlers.start import players
from keyboards import main_menu

async def animal_menu_callback(callback: types.CallbackQuery):
    """Показать меню покупки животных (вызывается из магазина)"""
    user = players.get(callback.from_user.id)
    if not user:
        await callback.message.edit_text(
            "❌ Сначала напиши /start",
            reply_markup=main_menu()
        )
        await callback.answer()
        return
    
    # Проверяем, есть ли животные
    has_animals = any(amount > 0 for amount in user.animals.values())
    
    if not has_animals:
        await callback.message.edit_text(
            f"🐄 У тебя нет животных!\n"
            f"💰 Денег: {user.money}$\n\n"
            f"Купи животных в 🏪 Магазине!",
            reply_markup=main_menu()
        )
    else:
        # Показываем, что есть
        animals_list = []
        for animal, amount in user.animals.items():
            if amount > 0:
                animals_list.append(f"{animal}: {amount} шт.")
        
        await callback.message.edit_text(
            f"🐄 Твои животные:\n" + "\n".join(animals_list) +
            f"\n\n💰 Денег: {user.money}$",
            reply_markup=main_menu()
        )
    await callback.answer()

async def buy_animal_callback(callback: types.CallbackQuery):
    """Обработка покупки животного (вызывается из магазина)"""
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
    
    # Возвращаемся в магазин
    from keyboards import shop_menu
    await callback.message.edit_text(
        message + "\n\n🏪 Вернуться в магазин",
        reply_markup=shop_menu()
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
    dp.callback_query.register(collect_products_callback, lambda c: c.data == "animal_products"),
