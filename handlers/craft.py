# handlers/craft.py
from aiogram import types
from aiogram.filters import Command
from handlers.start import players

RECIPES = {
    "🍞 Хлеб": {"ingredients": {"🌾Пшеница": 3}, "sell_price": 150},
    "🍰 Торт": {"ingredients": {"🌾Пшеница": 5, "🍓Клубника": 3}, "sell_price": 500},
    "🧃 Сок": {"ingredients": {"🍎Яблоко": 5}, "sell_price": 200},
    "🍷 Вино": {"ingredients": {"🍇Виноград": 10}, "sell_price": 800},
}

async def craft_command(message: types.Message):
    user = players.get(message.from_user.id)
    if not user:
        await message.answer("❌ /start")
        return
    
    text = "🧪 **Рецепты:**\n\n"
    for item, data in RECIPES.items():
        ingredients = ", ".join([f"{k} {v}шт" for k, v in data["ingredients"].items()])
        text += f"{item}: {ingredients} → продажа {data['sell_price']}$\n"
    
    await message.answer(text)

def register_craft(dp):
    dp.message.register(craft_command, Command("craft"))
