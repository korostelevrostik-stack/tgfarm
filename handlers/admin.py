from aiogram import types
from aiogram.filters import Command
from config import ADMIN_ID, CROP_DATA
from handlers.start import players
import time

class MutationSystem:
    def __init__(self):
        self.active_mutations = {}
        self.mutation_types = {
            "клубничная": {"emoji": "🍓", "multiplier": 2.0, "desc": "Урожайность x2"},
            "ядовитая": {"emoji": "☠️", "multiplier": 0.5, "desc": "Урожайность x0.5"},
            "светящаяся": {"emoji": "✨", "multiplier": 3.0, "desc": "Урожайность x3"},
            "радиационная": {"emoji": "☢️", "multiplier": 5.0, "desc": "Урожайность x5"},
            "золотая": {"emoji": "🌟", "multiplier": 10.0, "desc": "Урожайность x10"},
            "гигантская": {"emoji": "🐘", "multiplier": 1.5, "desc": "Урожайность x1.5"},
            "миниатюрная": {"emoji": "🐭", "multiplier": 0.3, "desc": "Урожайность x0.3"},
            "ледяная": {"emoji": "❄️", "multiplier": 0.7, "desc": "Урожайность x0.7"},
            "огненная": {"emoji": "🔥", "multiplier": 4.0, "desc": "Урожайность x4"},
            "призрачная": {"emoji": "👻", "multiplier": 2.5, "desc": "Урожайность x2.5"},
            "неоновая": {"emoji": "💡", "multiplier": 8.0, "desc": "Урожайность x8"},
            "кристальная": {"emoji": "💎", "multiplier": 6.0, "desc": "Урожайность x6"},
            "туманная": {"emoji": "🌫️", "multiplier": 0.9, "desc": "Урожайность x0.9"},
            "солнечная": {"emoji": "☀️", "multiplier": 7.0, "desc": "Урожайность x7"},
            "лунная": {"emoji": "🌙", "multiplier": 3.5, "desc": "Урожайность x3.5"},
            "звёздная": {"emoji": "⭐", "multiplier": 12.0, "desc": "Урожайность x12"},
            "радужная": {"emoji": "🌈", "multiplier": 4.5, "desc": "Урожайность x4.5"},
            "теневая": {"emoji": "🌑", "multiplier": 0.4, "desc": "Урожайность x0.4"},
            "механическая": {"emoji": "🤖", "multiplier": 9.0, "desc": "Урожайность x9"},
            "древняя": {"emoji": "🏛️", "multiplier": 15.0, "desc": "Урожайность x15"}
        }
        self.private_mutations = {}

    def get_active_mutations_text(self):
        if not self.active_mutations and not self.private_mutations:
            return "🔴 Нет активных мутаций"
        text = ""
        if self.active_mutations:
            text += "🧬 Глобальные мутации:\n"
            for name in self.active_mutations:
                emoji = self.mutation_types[name]["emoji"]
                mult = self.mutation_types[name]["multiplier"]
                text += f"{emoji} {name}: x{mult} (для всех)\n"
        if self.private_mutations:
            text += "\n👑 Личные мутации:\n"
            for name in self.private_mutations:
                emoji = self.mutation_types[name]["emoji"]
                mult = self.mutation_types[name]["multiplier"]
                text += f"{emoji} {name}: x{mult} (только для админа)\n"
        return text

mutation_system = MutationSystem()

async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    mutations_text = mutation_system.get_active_mutations_text()
    await message.answer(
        f"👑 Админ-панель\n\n"
        f"👤 Игроков: {len(players)}\n"
        f"💰 Денег: {sum(p.money for p in players.values())}$\n\n"
        f"{mutations_text}\n\n"
        f"📋 Команды:\n"
        f"/giveall 100 — дать всем денег\n"
        f"/resetall — сбросить всех\n"
        f"/players — список игроков\n"
        f"/global_mutate <название> — мутация для всех\n"
        f"/private_mutate <название> — только для тебя\n"
        f"/mutations — список активных мутаций\n"
        f"/clearmutations — убрать все мутации\n"
        f"/mutation_list — все доступные мутации"
    )

async def global_mutate(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    try:
        parts = message.text.split()
        if len(parts) < 2:
            await message.answer("❌ Использование: /global_mutate <название>\nДоступные мутации:\n" + "\n".join([f"{data['emoji']} {name} (x{data['multiplier']})" for name, data in mutation_system.mutation_types.items()]))
            return
        mutation_name = parts[1].lower()
        if mutation_name not in mutation_system.mutation_types:
            await message.answer(f"❌ Мутация '{mutation_name}' не найдена!")
            return
        mutation_system.active_mutations[mutation_name] = {"started": time.time(), "multiplier": mutation_system.mutation_types[mutation_name]["multiplier"]}
        emoji = mutation_system.mutation_types[mutation_name]["emoji"]
        mult = mutation_system.mutation_types[mutation_name]["multiplier"]
        for user_id in players.keys():
            try: await message.bot.send_message(user_id, f"🧬 ГЛОБАЛЬНАЯ МУТАЦИЯ!\n{emoji} {mutation_name} x{mult}\nВсе цены на урожай увеличены!")
            except: pass
        await message.answer(f"✅ Глобальная мутация активирована!\n{emoji} {mutation_name} x{mult}\n⏳ Действует 1 час (или пока не отключишь)")
    except Exception as e: await message.answer(f"❌ Ошибка: {e}")

async def private_mutate(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    try:
        parts = message.text.split()
        if len(parts) < 2:
            await message.answer("❌ Использование: /private_mutate <название>\nДоступные мутации:\n" + "\n".join([f"{data['emoji']} {name} (x{data['multiplier']})" for name, data in mutation_system.mutation_types.items()]))
            return
        mutation_name = parts[1].lower()
        if mutation_name not in mutation_system.mutation_types:
            await message.answer(f"❌ Мутация '{mutation_name}' не найдена!")
            return
        mutation_system.private_mutations[mutation_name] = {"started": time.time(), "multiplier": mutation_system.mutation_types[mutation_name]["multiplier"]}
        emoji = mutation_system.mutation_types[mutation_name]["emoji"]
        mult = mutation_system.mutation_types[mutation_name]["multiplier"]
        await message.answer(f"✅ Личная мутация активирована!\n{emoji} {mutation_name} x{mult}\n⏳ Только для тебя!")
    except Exception as e: await message.answer(f"❌ Ошибка: {e}")

async def list_mutations(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    text = "🧬 Доступные мутации:\n\n"
    for name, data in mutation_system.mutation_types.items():
        text += f"{data['emoji']} {name}: x{data['multiplier']} — {data['desc']}\n"
    await message.answer(text)

async def clear_all_mutations(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    mutation_system.active_mutations.clear(); mutation_system.private_mutations.clear()
    await message.answer("✅ Все мутации очищены!")

async def show_active_mutations(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    await message.answer(mutation_system.get_active_mutations_text())

async def give_all_money(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    try:
        amount = int(message.text.split()[1])
        for p in players.values(): p.money += amount
        await message.answer(f"✅ Выдал {amount}$ всем!")
    except: await message.answer("❌ /giveall 100")

async def reset_all(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    for p in players.values():
        p.money = 500
        p.crops = {c: 0 for c in p.crops}
        p.animals = {a: 0 for a in p.animals}
        p.day = 1
        p.total_sold = {}
        p.unlocked_crops = []
        for crop, data in CROP_DATA.items():
            if data.get("unlock_requirement", 0) == 0: p.unlocked_crops.append(crop)
    await message.answer("✅ Все сброшены!")

async def list_players(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    text = "👤 Игроки:\n"
    for uid, p in players.items():
        text += f"ID: {uid} | 💰 {p.money}$ | День {p.day} | 🔓 {len(p.unlocked_crops)} культур\n"
    await message.answer(text)

def register_admin(dp):
    dp.message.register(admin_panel, Command("admin"))
    dp.message.register(give_all_money, Command("giveall"))
    dp.message.register(reset_all, Command("resetall"))
    dp.message.register(list_players, Command("players"))
    dp.message.register(global_mutate, Command("global_mutate"))
    dp.message.register(private_mutate, Command("private_mutate"))
    dp.message.register(list_mutations, Command("mutation_list"))
    dp.message.register(clear_all_mutations, Command("clearmutations"))
    dp.message.register(show_active_mutations, Command("mutations"))
