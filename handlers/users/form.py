from loader import dp

from aiogram import types
from aiogram.types import ContentType
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from filters.is_right_type_answer import IsRightTypeAnswerFilter
from data.config import messages
from states.questionnaire_states import QuestionnaireState
from utils.saver import Saver
from keyboards.default.make_keyboard import make_keyboard


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
        await message.answer(messages['finish_message'])
        await send_report(state)
        await state.finish()
    else:
        new_id = question_id + 1
        text = messages['questions'][new_id]['text']
        markup = make_keyboard(messages['questions'][new_id])
        await state.update_data(question_id=new_id)
        await message.answer(text, reply_markup=markup)


@dp.message_handler(state=QuestionnaireState.IN_PROCESS)
async def send_wrong_answer(message: types.Message, state: FSMContext):
    text = messages['wrong_type_answer']
    await message.answer(text)


async def send_report(state):
    data = await state.get_data()
    text = '<b>Отчёт</b>'
    for question in messages['questions']:
        current_value = data[question['var']]
        text += f"\n<b>{question['var']}:</b> {current_value}"
    print(text)
