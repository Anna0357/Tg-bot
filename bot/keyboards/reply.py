from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Пройти тест"), KeyboardButton(text="О профессиях")],
            [KeyboardButton(text="Полезные ссылки")],
        ],
        resize_keyboard=True,
    )
