from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_markup():
    markup = ReplyKeyboardMarkup()
    markup.add(KeyboardButton("✅Заполнить анкету✅"))
    markup.add(KeyboardButton("📗Заполненные анкеты📗"))
    return markup
