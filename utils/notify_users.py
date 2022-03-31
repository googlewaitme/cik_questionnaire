from datetime import datetime, date, time
import logging
import asyncio

from aiogram import Dispatcher

from data.config import data
from utils.db_api.user_api import UserApi


def planing_notify_users(loop, dp: Dispatcher):
    day, month, year = [int(el) for el in data['date'].split('.')]
    report_date = date(year=year, month=month, day=day)
    for data_time in data['report_times']:
        hour, minute = data_time.split(':')
        report_time = time(int(hour), int(minute))
        report_datetime = datetime.combine(report_date, report_time)
        asyncio.ensure_future(notify_users(report_datetime, dp), loop=loop)


async def notify_users(report_time: datetime, dp: Dispatcher):
    now = datetime.now()
    if now > report_time:
        logging.info("Ignored to notify: " + str(report_time))
        return
    delta = report_time - datetime.now()
    seconds = delta.total_seconds()
    await asyncio.sleep(seconds)
    users = UserApi.get_all_users()
    for user in users:
        await dp.bot.send_message(
            user.telegram_id,
            'Необходимо заполнить анкету!')
