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
            final_price = int(base_cost * 1.2)  # 50 → 60, 80 → 96, 120 → 144
            
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
