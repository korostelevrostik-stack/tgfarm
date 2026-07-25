from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from handlers.start import players
from config import CROP_DATA
import random

class GuessGame(StatesGroup):
    playing = State()

class WheelGame(StatesGroup):
    spinning = State()

async def guess_start(message: types.Message, state: FSMContext):
    user = players.get(message.from_user.id)
    if not user: await message.answer("❌ Напиши /start"); return
    if user.money < 10: await message.answer("❌ Для игры нужно 10$!"); return
    user.money -= 10
    crop_list = list(CROP_DATA.keys())
    selected = random.choice(crop_list)
    emoji = CROP_DATA[selected]["emoji"]
    await state.update_data(answer=selected)
    await state.set_state(GuessGame.playing)
    options = [selected]
    while len(options) < 4:
        rand_crop = random.choice(crop_list)
        if rand_crop not in options: options.append(rand_crop)
    random.shuffle(options)
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=opt, callback_data=f"guess_{opt}") for opt in options[:2]],
        [types.InlineKeyboardButton(text=opt, callback_data=f"guess_{opt}") for opt in options[2:]]
    ])
    await message.answer(f"🎯 Угадай культуру!\n\nЭмодзи: {emoji}\n\nВыбери правильный ответ:", reply_markup=keyboard)

async def guess_answer(callback: types.CallbackQuery, state: FSMContext):
    user = players.get(callback.from_user.id)
    if not user: await callback.answer("❌ Ошибка!"); return
    data = await state.get_data()
    correct_answer = data.get("answer")
    user_choice = callback.data.replace("guess_", "")
    if user_choice == correct_answer:
        reward = random.randint(20, 50)
        user.money += reward
        await callback.message.edit_text(f"✅ Правильно! 🎉\n\nЭто {correct_answer}!\n💰 Ты выиграл {reward}$!\n💰 Всего: {user.money}$")
    else:
        await callback.message.edit_text(f"❌ Неправильно!\n\nПравильный ответ: {correct_answer}\n💰 У тебя осталось: {user.money}$\n\nПопробуй ещё раз: /guess")
    await state.clear()
    await callback.answer()

async def wheel_start(message: types.Message, state: FSMContext):
    user = players.get(message.from_user.id)
    if not user: await message.answer("❌ Напиши /start"); return
    if user.money < 20: await message.answer("❌ Для игры на колесе фортуны нужно 20$!"); return
    user.money -= 20
    await state.set_state(WheelGame.spinning)
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🎰 Крутить!", callback_data="spin_wheel")]
    ])
    await message.answer(f"🎰 Колесо фортуны!\n\n💰 Ставка: 20$\n🎁 Призы: 0$, 50$, 100$, 200$, 500$\n\nНажми на кнопку, чтобы крутить!", reply_markup=keyboard)

async def spin_wheel(callback: types.CallbackQuery, state: FSMContext):
    user = players.get(callback.from_user.id)
    if not user: await callback.answer("❌ Ошибка!"); return
    sectors = [0, 50, 100, 200, 500]
    weights = [30, 30, 20, 15, 5]
    result = random.choices(sectors, weights=weights)[0]
    if result > 0:
        user.money += result
        await callback.message.edit_text(f"🎰 Колесо фортуны!\n\n🎉 Тебе выпало: {result}$!\n💰 Всего: {user.money}$\n\nСыграть ещё: /wheel")
    else:
        await callback.message.edit_text(f"🎰 Колесо фортуны!\n\n😢 Тебе ничего не выпало...\n💰 Осталось: {user.money}$\n\nПопробуй ещё: /wheel")
    await state.clear()
    await callback.answer()

async def games_menu(message: types.Message):
    await message.answer(
        f"🎮 Мини-игры\n\n"
        f"1. 🎯 Угадай культуру — 10$ за игру, выигрыш 20-50$\n   Команда: /guess\n\n"
        f"2. 🎰 Колесо фортуны — 20$ за игру, выигрыш до 500$\n   Команда: /wheel\n\n"
        f"Выбирай и играй!"
    )

def register_minigames(dp):
    dp.message.register(games_menu, Command("games"))
    dp.message.register(guess_start, Command("guess"))
    dp.message.register(wheel_start, Command("wheel"))
    dp.callback_query.register(guess_answer, lambda c: c.data.startswith("guess_"))
    dp.callback_query.register(spin_wheel, lambda c: c.data == "spin_wheel")
