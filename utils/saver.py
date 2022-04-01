from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import messages

import logging


class Saver():
    def __init__(
            self, message: types.Message, state: FSMContext, question_id: int):
        self.message = message
        self.state = state
        self.question = messages['questions'][question_id]
        self.data_type = self.question['type_answer']
        self.variable_name = self.question['var']

    async def save(self):
        if self.data_type == 'str':
            await self.save_str()
        elif self.data_type == 'int':
            await self.save_int()
        elif self.data_type == 'float':
            await self.save_float()
        elif self.data_type == 'photo':
            await self.save_photo()
        elif self.data_type == 'choose':
            await self.save_str()
        elif self.data_type == 'video_note':
            await self.save_video_note()
        elif self.data_type == 'confirmation':
            await self.save_confirmation()
        else:
            logging.error('Not right data_type')


    async def save_photo(self):
        file_id = self.message.photo[-1]['file_id']
        await self.state.update_data({self.variable_name: file_id})

    async def save_int(self):
        await self.state.update_data({self.variable_name: self.message.text})

    async def save_float(self):
        await self.state.update_data({self.variable_name: self.message.text})

    async def save_str(self):
        await self.state.update_data({self.variable_name: self.message.text})

    async def save_video_note(self):
        file_id = self.message.video_note['file_id']
        await self.state.update_data({self.variable_name: file_id})

    async def save_confirmation(self):
        await self.state.update_data({self.variable_name: self.message.text})
