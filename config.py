import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN", "8973072159:AAHHqRXaDePf6qmB3muzfKypKh4JBOHWCFo")

START_MONEY = 500
FOOD_COST_PER_ANIMAL = 15
SELL_ANIMAL_PRICE = 50

CROP_DATA = {
    "🌾Пшеница": {"cost": 50, "sell": 80, "min_yield": 5, "max_yield": 15, "emoji": "🌾"},
    "🌽Кукуруза": {"cost": 80, "sell": 150, "min_yield": 5, "max_yield": 15, "emoji": "🌽"},
    "🍅Помидоры": {"cost": 120, "sell": 250, "min_yield": 5, "max_yield": 15, "emoji": "🍅"}
}

ANIMAL_DATA = {
    "🐔Куры": {"cost": 200, "product": "🥚", "min_prod": 1, "max_prod": 3, "price_per_unit": 10, "emoji": "🐔"},
    "🐄Коровы": {"cost": 500, "product": "🥛", "min_prod": 2, "max_prod": 5, "price_per_unit": 20, "emoji": "🐄"},
    "🐑Овцы": {"cost": 400, "product": "🧶", "min_prod": 1, "max_prod": 2, "price_per_unit": 30, "emoji": "🐑"}
}

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///farm.db")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ADMIN_ID = 8261666607  # ← ТВОЙ ID
