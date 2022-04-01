import csv
import os

from loader import dp

from aiogram import types
from aiogram.types import ContentType
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from handlers.users import menu
from filters.is_right_type_answer import IsRightTypeAnswerFilter
from data.config import messages
from states.questionnaire_states import QuestionnaireState
from utils.saver import Saver
from utils.db_api.user_api import UserApi
from keyboards.default.make_keyboard import make_keyboard
from keyboards.default import menu_keyboard


@dp.message_handler(Text("📗Заполненные анкеты📗"))
async def send_answer_about_development(message: types.Message):
    await message.answer("Пока в разработке")


@dp.message_handler(Text('✅Заполнить анкету✅'))
async def set_questionnaire_state(message: types.Message, state: FSMContext):
    markup = make_keyboard(messages['questions'][0])
    text = messages['questions'][0]['text']
    await message.answer(text, reply_markup=markup)
    await QuestionnaireState.IN_PROCESS.set()
    await state.update_data(question_id=0)


@dp.message_handler(
    IsRightTypeAnswerFilter(),
    content_types=ContentType.ANY,
    state=QuestionnaireState.IN_PROCESS
)
async def send_next_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    question_id = data['question_id']
    saver = Saver(message, state, question_id)
    await saver.save()
    count_of_questions = len(messages['questions'])
    if question_id + 1 == count_of_questions:
        # if it last question
        markup = menu_keyboard.get_markup()
        await message.answer(
            messages['finish_message'],
            reply_markup=markup)
        await send_report(message.from_user.id, state)
        await state.finish()
    else:
        data = await state.get_data()
        new_id = question_id + 1
        text = messages['questions'][new_id]['text'].format(**data)
        markup = make_keyboard(messages['questions'][new_id])
        await state.update_data(question_id=new_id)
        await message.answer(text, reply_markup=markup)


@dp.message_handler(state=QuestionnaireState.IN_PROCESS)
async def send_wrong_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if 'to_end_state' in data and data['to_end_state'] is True:
        await state.finish()
        await menu.send_menu(message, state)
    else:
        text = messages['wrong_type_answer']
        await message.answer(text)


async def send_report(telegram_id, state):
    name = UserApi(telegram_id).get_name()
    data = await state.get_data()
    to_write_in_csv = {'Имя': name}
    for question in messages['questions']:
        current_value = data[question['var']]
        to_write_in_csv[question['var']] = current_value
    write_in_csv(to_write_in_csv)


def write_in_csv(data):
    with open('output.csv', 'a') as output_file:
        writer = csv.DictWriter(
            output_file, dialect='excel', fieldnames=data.keys())
        if os.stat('output.csv').st_size == 0:
            writer.writeheader()
        writer.writerow(data)
        output_file.close()
