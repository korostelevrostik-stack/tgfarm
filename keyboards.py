# keyboards.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import CROP_DATA, ANIMAL_DATA

def main_menu():
    """Главное меню — 3 кнопки"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌱 Посадить", callback_data="plant")],
        [InlineKeyboardButton(text="🧺 Собрать урожай", callback_data="harvest")],
        [InlineKeyboardButton(text="🏪 Магазин", callback_data="shop")]
    ])

def shop_menu():
    """Меню магазина — семена, животные, назад"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌾 Купить семена", callback_data="buy_seeds")],
        [InlineKeyboardButton(text="🐄 Купить животных", callback_data="buy_animals")],
        [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back")]
    ])

def seeds_menu():
    """Меню семян"""
    buttons = []
    for crop, data in CROP_DATA.items():
        buttons.append([
            InlineKeyboardButton(
                text=f"{crop} ({data['cost']}$)", 
                callback_data=f"plant_{crop}"
            )
        ])
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_shop")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def animals_shop_menu():
    """Меню покупки животных"""
    buttons = []
    for animal, data in ANIMAL_DATA.items():
        buttons.append([
            InlineKeyboardButton(
                text=f"{animal} ({data['cost']}$)", 
                callback_data=f"buy_{animal}"
            )
        ])
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_shop")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def back_to_shop():
    """Кнопка назад в магазин"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад в магазин", callback_data="back_shop")]
    ])
