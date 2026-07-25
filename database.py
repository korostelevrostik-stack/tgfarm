import sqlite3
import json
from config import START_MONEY

DB_NAME = 'farm.db'

def get_db():
    """Подключение к базе данных"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Создание таблиц при первом запуске"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Таблица игроков
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            user_id INTEGER PRIMARY KEY,
            money INTEGER DEFAULT 500,
            day INTEGER DEFAULT 1,
            crops TEXT DEFAULT '{}',
            animals TEXT DEFAULT '{}',
            total_sold TEXT DEFAULT '{}',
            unlocked_crops TEXT DEFAULT '[]',
            daily_streak INTEGER DEFAULT 0,
            last_daily TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ База данных инициализирована!")

def save_player(player):
    """Сохранить игрока в базу"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR REPLACE INTO players (
            user_id, money, day, crops, animals, total_sold, unlocked_crops,
            daily_streak, last_daily
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        player.id,
        player.money,
        player.day,
        json.dumps(player.crops),
        json.dumps(player.animals),
        json.dumps(player.total_sold),
        json.dumps(player.unlocked_crops),
        getattr(player, 'daily_streak', 0),
        getattr(player, 'last_daily', None)
    ))
    conn.commit()
    conn.close()

def load_player(user_id):
    """Загрузить игрока из базы"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM players WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            'money': row['money'],
            'day': row['day'],
            'crops': json.loads(row['crops']),
            'animals': json.loads(row['animals']),
            'total_sold': json.loads(row['total_sold']),
            'unlocked_crops': json.loads(row['unlocked_crops']),
            'daily_streak': row['daily_streak'],
            'last_daily': row['last_daily']
        }
    return None

def delete_player(user_id):
    """Удалить игрока (для сброса)"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM players WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

def get_all_players():
    """Получить всех игроков для топа"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, money, day FROM players ORDER BY money DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_player_money(user_id, amount):
    """Обновить деньги игрока"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE players SET money = ? WHERE user_id = ?', (amount, user_id))
    conn.commit()
    conn.close()
