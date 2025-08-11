import telebot
from telebot import types
from config import TOKEN
import random
from datetime import datetime

bot = telebot.TeleBot(TOKEN)

# Расширенная база героев с предметами
heroes = {
    "pudge": {
        "name": "Pudge",
        "role": "Tank/Disabler",
        "difficulty": "Средняя",
        "ult": "Dismember (пожирает врага)",
        "items": ["Bottle", "Blink Dagger", "Aghanim's Scepter", "Heart of Tarrasque"]
    },
    "invoker": {
        "name": "Invoker",
        "role": "Nuker/Disabler",
        "difficulty": "Очень высокая",
        "ult": "Invoke (меняет заклинания)",
        "items": ["Hand of Midas", "Scythe of Vyse", "Aghanim's Scepter", "Octarine Core"]
    },
    "anti-mage": {
        "name": "Anti-Mage",
        "role": "Carry",
        "difficulty": "Легкий",
        "ult": "Mana Void (чем меньше маны, тем больше урона)",
        "items": ["Power Treads", "Battle Fury", "Manta Style", "Abyssal Blade"]
    },
    "zeus": {
        "name": "Zeus",
        "role": "Nuker",
        "difficulty": "Легкая",
        "ult": "Thundergod's Wrath (бьёт всех врагов на карте)",
        "items": ["Arcane Boots", "Aether Lens", "Aghanim's Scepter", "Refresher Orb"]
    },
    "juggernaut": {
        "name": "Juggernaut",
        "role": "Carry",
        "difficulty": "Средняя",
        "ult": "Omnislash (множественные атаки)",
        "items": ["Phase Boots", "Battle Fury", "Manta Style", "Butterfly"]
    },
    "witch doctor": {
        "name": "Witch Doctor",
        "role": "Support",
        "difficulty": "Средняя",
        "ult": "Death Ward (мощная неподвижная атака)",
        "items": ["Arcane Boots", "Glimmer Cape", "Aghanim's Scepter", "Octarine Core"]
    },
    "puck": {
        "name": "Puck",
        "role": "Initiator/Nuker",
        "difficulty": "Высокая",
        "ult": "Dream Coil (оглушает при разрыве связи)",
        "items": ["Tranquil Boots", "Blink Dagger", "Dagon", "Eul's Scepter"]
    },
    "mars": {
        "name": "Mars",
        "role": "Initiator/Tank",
        "difficulty": "Средняя",
        "ult": "Arena of Blood (создает арену для боя)",
        "items": ["Phase Boots", "Blink Dagger", "Black King Bar", "Desolator"]
    },
    "morphling": {
        "name": "Morphling",
        "role": "Carry",
        "difficulty": "Очень высокая",
        "ult": "Morph (копирует героя)",
        "items": ["Power Treads", "Ethereal Blade", "Eye of Skadi", "Linken's Sphere"]
    }
}

# Информация о последнем патче
current_patch = {
    "version": "7.39d",
    "date": "06.08.2025",
    "changes": [
        "Maelstrom - Chain Lightning: больше не наносит увеличенный урон иллюзиям",
        "Изменения предметов - Blade Mail - Бонус к урону уменьшен с 18 до 15 - Damage Return: пассивное отражение урона от атак уменьшено с 20 + 20% до 10 + 15%",
        "Puck - Прирост ловкости уменьшен с 2,5 до 2,3",
        "Изменения ландшафта - Убрано непредусмотренное место для варда в сложном лагере возле лёгкой линии сил Света"
    ]
}

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        types.KeyboardButton("Рандомный герой"),
        types.KeyboardButton("Список героев"),
        types.KeyboardButton("Помощь"),
        types.KeyboardButton("Текущий патч")
    ]
    markup.add(*buttons)
    
    welcome_text = (
        "🎮 *Dota 2 Helper Bot*\n\n"
        "Я помогу вам с информацией о героях и обновлениях Dota 2!\n\n"
        "Доступные команды:\n"
        "/hero [имя] - информация о герое\n"
        "/items [имя] - предметы для героя\n"
        "/random - случайный герой\n"
        "/patch - текущее обновление\n"
        "/allheroes - список всех героев"
    )
    
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown', reply_markup=markup)

# Команда /hero
@bot.message_handler(commands=['hero'])
def hero(message):
    if len(message.text.split()) < 2:
        bot.send_message(message.chat.id, "Используйте: /hero [имя героя]\nПример: /hero Zeus")
        return
    
    hero_name = " ".join(message.text.split()[1:]).lower()
    hero_data = None
    
    for key in heroes:
        if hero_name.replace("-", "").replace(" ", "") == key.replace("-", "").replace(" ", ""):
            hero_data = heroes[key]
            break
    
    if hero_data:
        response = (
            f"⚔️ *{hero_data['name']}*\n"
            f"▫️ Роль: {hero_data['role']}\n"
            f"▫️ Сложность: {hero_data['difficulty']}\n"
            f"▫️ Ультимативная способность: {hero_data['ult']}\n"
            f"▫️ Предметы: /items_{key}"
        )
        bot.send_message(message.chat.id, response, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "Герой не найден. Используйте /allheroes для списка героев")

# Команда /items
@bot.message_handler(commands=['items'])
def items(message):
    if len(message.text.split()) < 2:
        bot.send_message(message.chat.id, "Используйте: /items [имя героя]\nПример: /items Witch Doctor")
        return
    
    hero_name = " ".join(message.text.split()[1:]).lower()
    hero_data = None
    
    for key in heroes:
        if hero_name.replace("-", "").replace(" ", "") == key.replace("-", "").replace(" ", ""):
            hero_data = heroes[key]
            break
    
    if hero_data:
        items_list = "\n".join([f"{i+1}. {item}" for i, item in enumerate(hero_data['items'])])
        response = (
            f"🛒 *Рекомендуемые предметы для {hero_data['name']}*\n\n"
            f"{items_list}\n\n"
            f"Последние изменения в патче: /patch"
        )
        bot.send_message(message.chat.id, response, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "Герой не найден. Используйте /allheroes для списка героев")

# Команда /random
@bot.message_handler(commands=['random'])
def random_hero(message):
    hero_name, hero_data = random.choice(list(heroes.items()))
    response = (
        f"🎲 *Случайный герой: {hero_data['name']}*\n\n"
        f"▫️ Роль: {hero_data['role']}\n"
        f"▫️ Сложность: {hero_data['difficulty']}\n"
        f"▫️ Ульт: {hero_data['ult']}\n\n"
        f"Предметы: /items_{hero_name}\n"
        f"Полная информация: /hero {hero_data['name']}"
    )
    bot.send_message(message.chat.id, response, parse_mode='Markdown')

# Команда /patch
@bot.message_handler(commands=['patch'])
def show_patch(message):
    changes_list = "\n".join([f"▪ {change}" for change in current_patch['changes']])
    response = (
        f"🔄 *Текущее обновление Dota 2 {current_patch['version']}*\n"
        f"Дата выхода: {current_patch['date']}\n\n"
        f"*Основные изменения:*\n"
        f"{changes_list}\n\n"
        f"Для информации о героях используйте /hero [имя]"
    )
    bot.send_message(message.chat.id, response, parse_mode='Markdown')

# Команда /allheroes
@bot.message_handler(commands=['allheroes'])
def all_heroes(message):
    hero_list = "\n".join([f"▪ {hero['name']} - /hero_{key} /items_{key}" for key, hero in heroes.items()])
    response = (
        "📜 *Список всех героев в базе:*\n\n"
        f"{hero_list}\n\n"
        "Используйте команды /hero или /items с именем героя для подробной информации"
    )
    bot.send_message(message.chat.id, response, parse_mode='Markdown')

# Обработка кнопок
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == "Рандомный герой":
        random_hero(message)
    elif message.text == "Список героев":
        all_heroes(message)
    elif message.text == "Помощь":
        start(message)
    elif message.text == "Текущий патч":
        show_patch(message)

# Запуск бота
if __name__ == '__main__':
    print(f"Бот запущен в {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    bot.polling(none_stop=True)
