from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import ReplyKeyboardRemove


def make_keyboard(question):
    if question['type_answer'] == 'choose':
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        for text_button in question['answers']:
            markup.row(KeyboardButton(text_button))
    else:
        markup = ReplyKeyboardRemove()
    return markup
