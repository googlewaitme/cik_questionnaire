from aiogram import types
from aiogram.dispatcher.filters import Filter
from aiogram.dispatcher import FSMContext

from data.config import messages
from loader import dp


class IsRightTypeAnswerFilter(Filter):
    key = 'is_right_type_answer'

    async def check(self, message: types.Message):
        state = dp.current_state(user=message.from_user.id)
        data = await state.get_data()
        question_id = data['question_id']
        question = messages['questions'][question_id]
        need_type = question['type_answer']
        if need_type == 'str':
            return self.check_str(message, state)
        if need_type == 'int':
            return self.check_int(message, state)
        if need_type == 'float':
            return self.check_float(message, state)
        if need_type == 'photo':
            return self.check_photo(message, state)
        if need_type == 'video_note':
            return self.check_video(message, state)
        if need_type == 'choose':
            return self.check_choose(message, state, question)

    def check_int(self, message: types.Message, state: FSMContext):
        return message.text.isdigit()

    def check_float(self, message: types.Message, state: FSMContext):
        return message.text.replace('.', '', 1).isdigit()

    def check_str(self, message: types.Message, state: FSMContext):
        return message.text is not None

    def check_photo(self, message: types.Message, state: FSMContext):
        return message.photo

    def check_choose(
            self, message: types.Message, state: FSMContext, question: dict):
        return message.text in question['answers']

    def check_video(self, message: types.Message, state: FSMContext):
        return message.video_note
