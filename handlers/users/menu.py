from loader import dp

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from data.config import messages
from keyboards.default import menu_keyboard


@dp.message_handler(Text("меню"), state='*')
async def send_menu(message: types.Message, state: FSMContext):
    await state.finish()
    markup = menu_keyboard.get_markup()
    await message.answer(messages['menu_message'], reply_markup=markup)
