from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import CROP_DATA, ANIMAL_DATA

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌱 Посадить", callback_data="plant")],
        [InlineKeyboardButton(text="🧺 Собрать урожай", callback_data="harvest")],
        [InlineKeyboardButton(text="🏪 Магазин", callback_data="shop")]
    ])

def shop_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌾 Купить семена", callback_data="buy_seeds")],
        [InlineKeyboardButton(text="🐄 Купить животных", callback_data="buy_animals")],
        [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back")]
    ])

def seeds_menu(user):
    """Меню семян с учётом разблокировки"""
    buttons = []
    for crop, data in CROP_DATA.items():
        if user.check_unlock(crop):
            buttons.append([InlineKeyboardButton(
                text=f"{crop} ({data['cost']}$)", 
                callback_data=f"plant_{crop}"
            )])
        else:
            req = data.get("unlock_requirement", 0)
            unlock_crop = data.get("unlock_crop", "")
            buttons.append([InlineKeyboardButton(
                text=f"🔒 {crop} (нужно {req} {unlock_crop})", 
                callback_data="locked"
            )])
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_shop")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def animals_shop_menu():
    buttons = []
    for animal, data in ANIMAL_DATA.items():
        buttons.append([InlineKeyboardButton(
            text=f"{animal} ({data['cost']}$)", 
            callback_data=f"buy_{animal}"
        )])
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_shop")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def back_to_shop():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад в магазин", callback_data="back_shop")]
    ])
