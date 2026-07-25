import random
from config import CROP_DATA, ANIMAL_DATA, FOOD_COST_PER_ANIMAL, START_MONEY, SELL_ANIMAL_PRICE

class Player:
    def __init__(self, user_id):
        self.id = user_id
        self.money = START_MONEY
        self.crops = {crop: 0 for crop in CROP_DATA.keys()}
        self.animals = {animal: 0 for animal in ANIMAL_DATA.keys()}
        self.day = 1
    
    def plant_crop(self, crop_name):
        data = CROP_DATA[crop_name]
        if self.money < data["cost"]:
            return False, f"❌ Денег нет! Нужно {data['cost']}$"
        self.money -= data["cost"]
        yield_amount = random.randint(data["min_yield"], data["max_yield"])
        self.crops[crop_name] += yield_amount
        return True, f"✅ Посажено! Урожай: {yield_amount} шт."
    
    def harvest_all(self):
        from handlers.admin import mutation_system
        
        total_earn = 0
        messages = []
        
        for crop, amount in self.crops.items():
            if amount > 0:
                data = CROP_DATA[crop]
                base_cost = data["cost"]
                
                # ===== НОВАЯ ЭКОНОМИКА =====
                # Продажа = покупка × 1.2 (+20%)
                final_price = int(base_cost * 1.2)
                
                # Проверяем глобальные мутации
                for mutation_name in mutation_system.active_mutations:
                    if mutation_name in mutation_system.mutation_types:
                        final_price = int(final_price * mutation_system.mutation_types[mutation_name]["multiplier"])
                
                # Проверяем личные мутации (только админ)
                from config import ADMIN_ID
                if self.id == ADMIN_ID:
                    for mutation_name in mutation_system.private_mutations:
                        if mutation_name in mutation_system.mutation_types:
                            final_price = int(final_price * mutation_system.mutation_types[mutation_name]["multiplier"])
                
                earn = amount * final_price
                total_earn += earn
                
                messages.append(
                    f"{data['emoji']} {crop}: {amount}шт → +{earn}$ "
                    f"(по {final_price}$ за шт.)"
                )
                self.crops[crop] = 0
        
        if total_earn == 0:
            return 0, "😴 Урожая нет!"
        
        self.money += total_earn
        return total_earn, "\n".join(messages)
    
    def buy_animal(self, animal_name):
        data = ANIMAL_DATA[animal_name]
        if self.money < data["cost"]:
            return False, f"❌ Денег нет! Нужно {data['cost']}$"
        self.money -= data["cost"]
        self.animals[animal_name] += 1
        return True, f"✅ Куплено! Теперь {self.animals[animal_name]} шт."
    
    def collect_products(self):
        total_earn = 0
        messages = []
        for animal, count in self.animals.items():
            if count > 0:
                data = ANIMAL_DATA[animal]
                products = count * random.randint(data["min_prod"], data["max_prod"])
                earn = products * data["price_per_unit"]
                total_earn += earn
                messages.append(f"{data['product']} {animal}: {products} ед. (+{earn}$)")
        if total_earn == 0:
            return 0, "😢 Животных нет!"
        self.money += total_earn
        return total_earn, "\n".join(messages)
    
    def next_day(self):
        self.day += 1
        total_animals = sum(self.animals.values())
        if total_animals == 0:
            return f"⏩ День {self.day}\n😴 Животных нет."
        food_cost = total_animals * FOOD_COST_PER_ANIMAL
        if self.money >= food_cost:
            self.money -= food_cost
            return f"⏩ День {self.day}\n🍽️ Покормил (-{food_cost}$)"
        else:
            for animal in self.animals:
                if self.animals[animal] > 0:
                    self.animals[animal] -= 1
                    self.money += SELL_ANIMAL_PRICE
                    return f"⏩ День {self.day}\n😭 Продал {animal} за {SELL_ANIMAL_PRICE}$"
    
    def get_stats(self):
        from handlers.admin import mutation_system
        
        stats = [f"📅 День: {self.day}", f"💰 Денег: {self.money}$", "\n🌾 Урожай:"]
        has_crops = False
        for crop, amount in self.crops.items():
            if amount > 0:
                stats.append(f"  {crop}: {amount}шт")
                has_crops = True
        if not has_crops:
            stats.append("  Пусто")
        stats.append("\n🐄 Животные:")
        has_animals = False
        for animal, amount in self.animals.items():
            if amount > 0:
                stats.append(f"  {animal}: {amount}шт")
                has_animals = True
        if not has_animals:
            stats.append("  Пусто")
        
        if mutation_system.active_mutations:
            stats.append("\n🧬 **Активные мутации:**")
            for name, data in mutation_system.active_mutations.items():
                emoji = mutation_system.mutation_types[name]["emoji"]
                mult = mutation_system.mutation_types[name]["multiplier"]
                stats.append(f"  {emoji} {name}: x{mult}")
        
        return "\n".join(stats)
