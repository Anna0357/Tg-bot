from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def quiz_options_keyboard(question_index: int, option_labels: list[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i, label in enumerate(option_labels):
        builder.row(
            InlineKeyboardButton(
                text=label,
                callback_data=f"quiz:{question_index}:{i}",
            )
        )
    return builder.as_markup()
