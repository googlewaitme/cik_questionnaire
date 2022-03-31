from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.notify_users import planing_notify_users


from data import config
from utils.db_api.models import create_tables

import asyncio


loop = asyncio.get_event_loop()

create_tables()


bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

planing_notify_users(loop, dp)
