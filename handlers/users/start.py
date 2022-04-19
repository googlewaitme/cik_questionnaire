from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp

from keyboards.default import menu_keyboard


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    markup = menu_keyboard.get_markup()
    await message.answer(
        f"Здравствуйте, {message.from_user.full_name}!", reply_markup=markup)
