# utils.py
from config import CROP_DATA, ANIMAL_DATA

def format_money(amount):
    """Форматирование денег с разделителями"""
    return f"{amount:,}$".replace(",", " ")

def get_crop_emoji(crop_name):
    """Получить эмодзи для культуры"""
    return CROP_DATA.get(crop_name, {}).get("emoji", "🌱")

def get_animal_emoji(animal_name):
    """Получить эмодзи для животного"""
    return ANIMAL_DATA.get(animal_name, {}).get("emoji", "🐾")

def get_crop_sell_price(crop_name):
    """Получить цену продажи культуры"""
    return CROP_DATA.get(crop_name, {}).get("sell", 0)

def get_animal_product_price(animal_name):
    """Получить цену продукции животного"""
    return ANIMAL_DATA.get(animal_name, {}).get("price_per_unit", 0)

def get_total_animals(animals_dict):
    """Получить общее количество животных"""
    return sum(animals_dict.values())

def get_total_crops(crops_dict):
    """Получить общее количество урожая"""
    return sum(crops_dict.values())

def is_empty_dict(dictionary):
    """Проверить, пустой ли словарь (все значения = 0)"""
    return all(value == 0 for value in dictionary.values())
