from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from utils.db_api.user_api import UserApi as User


class AutorizationMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        telegram_id = message.from_user.id
        user = User(telegram_id)
        if user.is_exist():
            return
        if user.is_login(message.text):
            user.create()
            name = user.name
            await message.answer(f'Вы успешно авторизованы как: {name}')
            return
        await message.answer("Требуется авторизация. Отправьте пароль")
        raise CancelHandler()
