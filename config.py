# config.py
import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv("(2).env")

# ========== ТОКЕН БОТА ==========
TOKEN = os.getenv("BOT_TOKEN", "8973072159:AAHHqRXaDePf6qmB3muzfKypKh4JBOHWCFo")

# ========== НАСТРОЙКИ ИГРЫ ==========
START_MONEY = 500
FOOD_COST_PER_ANIMAL = 15
SELL_ANIMAL_PRICE = 50  # Сколько получаем при принудительной продаже

# ========== КУЛЬТУРЫ ==========
CROP_DATA = {
    "🌾Пшеница": {
        "cost": 50,           # Цена покупки
        "sell": 80,           # Цена продажи за 1 шт
        "min_yield": 5,       # Минимальный урожай
        "max_yield": 15,      # Максимальный урожай
        "emoji": "🌾"
    },
    "🌽Кукуруза": {
        "cost": 80,
        "sell": 150,
        "min_yield": 5,
        "max_yield": 15,
        "emoji": "🌽"
    },
    "🍅Помидоры": {
        "cost": 120,
        "sell": 250,
        "min_yield": 5,
        "max_yield": 15,
        "emoji": "🍅"
    }
}

# ========== ЖИВОТНЫЕ ==========
ANIMAL_DATA = {
    "🐔Куры": {
        "cost": 200,          # Цена покупки
        "product": "🥚",      # Что дают
        "min_prod": 1,        # Минимальное кол-во продукции
        "max_prod": 3,        # Максимальное кол-во продукции
        "price_per_unit": 10, # Цена за единицу продукции
        "emoji": "🐔"
    },
    "🐄Коровы": {
        "cost": 500,
        "product": "🥛",
        "min_prod": 2,
        "max_prod": 5,
        "price_per_unit": 20,
        "emoji": "🐄"
    },
    "🐑Овцы": {
        "cost": 400,
        "product": "🧶",
        "min_prod": 1,
        "max_prod": 2,
        "price_per_unit": 30,
        "emoji": "🐑"
    }
}

# ========== НАСТРОЙКИ БАЗЫ ДАННЫХ ==========
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///farm.db")

# ========== РЕЖИМ ОТЛАДКИ ==========
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# ========== ДРУГИЕ НАСТРОЙКИ ==========
MAX_PLAYERS_IN_RATING = 10  # Сколько игроков показывать в топе
