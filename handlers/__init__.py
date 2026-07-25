from . import start, plant, harvest, animals, day, stats, admin, minigames

def register_all_handlers(dp):
    start.register_start(dp)
    plant.register_plant(dp)
    harvest.register_harvest(dp)
    animals.register_animals(dp)
    day.register_day(dp)
    stats.register_stats(dp)
    admin.register_admin(dp)
    minigames.register_minigames(dp)  # ← ДОБАВИЛИ
