from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

_OPTION_LETTERS = ("А", "Б", "В", "Г")


def quiz_options_keyboard(question_index: int, num_options: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i in range(num_options):
        letter = _OPTION_LETTERS[i] if i < len(_OPTION_LETTERS) else str(i + 1)
        builder.row(
            InlineKeyboardButton(
                text=letter,
                callback_data=f"quiz:{question_index}:{i}",
            )
        )
    return builder.as_markup()
