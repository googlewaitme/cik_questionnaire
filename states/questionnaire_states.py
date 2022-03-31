from aiogram.dispatcher.filters.state import StatesGroup, State


class QuestionnaireState(StatesGroup):
    IN_PROCESS = State()
