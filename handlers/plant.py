from aiogram import types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from handlers.start import players
from keyboards import main_menu, shop_menu, seeds_menu
from config import CROP_DATA

class BuySeeds(StatesGroup):
    choosing_seed = State()
    entering_quantity = State()

async def plant_menu(callback: types.CallbackQuery, state: FSMContext):
    """Показать меню посадки"""
    user = players.get(callback.from_user.id)
    if not user:
        await callback.message.edit_text("❌ /start", reply_markup=main_menu())
        await callback.answer()
        return
    
    await state.set_state(BuySeeds.choosing_seed)
    await callback.message.edit_text(
        f"🌾 Выбери семена:\n💰 {user.money}$",
        reply_markup=seeds_menu()
    )
    await callback.answer()

async def choose_seed(callback: types.CallbackQuery, state: FSMContext):
    """Выбор семян → запрос количества"""
    user = players.get(callback.from_user.id)
    if not user:
        await callback.message.edit_text("❌ /start", reply_markup=main_menu())
        await callback.answer()
        return
    
    crop_name = callback.data.replace("plant_", "")
    crop_data = CROP_DATA[crop_name]
    
    await state.update_data(crop_name=crop_name, crop_cost=crop_data["cost"])
    await state.set_state(BuySeeds.entering_quantity)
    
    await callback.message.edit_text(
        f"🌾 {crop_name}\n"
        f"💰 Цена: {crop_data['cost']}$ за 1 шт.\n"
        f"💰 У тебя: {user.money}$\n\n"
        f"✏️ Введи **количество** (цифрой):",
        reply_markup=None
    )
    await callback.answer()

async def process_quantity(message: types.Message, state: FSMContext):
    """Обработка введённого количества"""
    user = players.get(message.from_user.id)
    if not user:
        await message.answer("❌ Напиши /start")
        await state.clear()
        return
    
    try:
        quantity = int(message.text.strip())
        if quantity <= 0:
            await message.answer("❌ Введи число больше 0!")
            return
        
        data = await state.get_data()
        crop_name = data.get("crop_name")
        crop_cost = data.get("crop_cost")
        
        if not crop_name:
            await message.answer("❌ Ошибка! Попробуй сначала.", reply_markup=main_menu())
            await state.clear()
            return
        
        total_cost = quantity * crop_cost
        
        if user.money < total_cost:
            await message.answer(
                f"❌ Не хватает денег!\n"
                f"Нужно: {total_cost}$\n"
                f"У тебя: {user.money}$\n\n"
                f"Попробуй меньше!",
                reply_markup=main_menu()
            )
            await state.clear()
            return
        
        user.money -= total_cost
        user.crops[crop_name] += quantity
        
        await message.answer(
            f"✅ Куплено {quantity} шт. {crop_name}!\n"
            f"💰 Снято: {total_cost}$\n"
            f"💰 Осталось: {user.money}$\n\n"
            f"🌱 Всего {crop_name}: {user.crops[crop_name]} шт.",
            reply_markup=main_menu()
        )
        
    except ValueError:
        await message.answer("❌ Введи **число** (например: 5)")
        return
    
    await state.clear()

async def cancel_buy(message: types.Message, state: FSMContext):
    """Отмена покупки"""
    await state.clear()
    await message.answer("🚫 Покупка отменена", reply_markup=main_menu())

def register_plant(dp):
    dp.callback_query.register(plant_menu, lambda c: c.data == "plant")
    dp.callback_query.register(choose_seed, lambda c: c.data.startswith("plant_"))
    dp.message.register(process_quantity, StateFilter(BuySeeds.entering_quantity))
    dp.message.register(cancel_buy, Command("cancel"))
