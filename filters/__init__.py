from loader import dp
from .is_right_type_answer import IsRightTypeAnswerFilter


if __name__ == "filters":
    dp.filters_factory.bind(IsRightTypeAnswerFilter)
