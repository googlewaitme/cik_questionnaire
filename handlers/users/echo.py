from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp

from keyboards.default import menu_keyboard


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    markup = menu_keyboard.get_markup()
    await message.answer('Меню', reply_markup=markup)


# Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
@dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    markup = menu_keyboard.get_markup()
    await state.finish()
    await message.answer('меню', reply_markup=markup)
