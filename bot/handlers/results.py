from aiogram.types import CallbackQuery, Message

from bot.keyboards.reply import main_menu_keyboard
from bot.services.scoring import (
    build_directions_message,
    build_hobbies_message,
    load_hobbies_by_direction,
    load_professions,
    primary_direction_id,
)


async def send_test_outcome_from_callback(
    callback: CallbackQuery,
    accumulated: dict[str, int],
) -> None:
    if not callback.message:
        return
    await send_test_outcome(callback.message, accumulated)


async def send_test_outcome(message: Message, accumulated: dict[str, int]) -> None:
    professions = load_professions()
    hobbies_map = load_hobbies_by_direction()
    primary = primary_direction_id(accumulated)

    await message.answer(
        build_directions_message(accumulated, professions),
        reply_markup=main_menu_keyboard(),
    )
    await message.answer(
        build_hobbies_message(primary, professions, hobbies_map),
        reply_markup=main_menu_keyboard(),
    )
