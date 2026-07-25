# handlers/__init__.py
from . import start, plant, harvest, animals, day, stats

def register_all_handlers(dp):
    """Регистрируем все обработчики команд и колбэков"""
    start.register_start(dp)
    plant.register_plant(dp)
    harvest.register_harvest(dp)
    animals.register_animals(dp)
    day.register_day(dp)
    stats.register_stats(dp)
