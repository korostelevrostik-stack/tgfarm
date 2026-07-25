# handlers/events.py
import random
from handlers.start import players

async def random_event(user):
    """Случайное событие"""
    events = [
        {"name": "🌧️ Дождь", "effect": "Урожай +20%", "bonus": 1.2},
        {"name": "☀️ Засуха", "effect": "Урожай -30%", "bonus": 0.7},
        {"name": "🎪 Ярмарка", "effect": "Цены х2", "bonus": 2.0},
    ]
    
    event = random.choice(events)
    # Применяем эффект на 1 день
    user.event_bonus = event["bonus"]
    user.event_name = event["name"]
    
    # Уведомляем игрока
    return f"⚠️ **Случайное событие!**\n{event['name']}: {event['effect']}"
