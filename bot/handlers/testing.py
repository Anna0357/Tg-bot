from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.handlers.results import send_test_outcome_from_callback
from bot.keyboards.inline import quiz_options_keyboard
from bot.keyboards.reply import main_menu_keyboard
from bot.services.scoring import empty_scores, load_quiz, merge_scores
from bot.states.orientation import OrientationStates

router = Router(name="testing")

_QUESTIONS = load_quiz()
_STATES = (
    OrientationStates.question_1,
    OrientationStates.question_2,
    OrientationStates.question_3,
)


def _question_text(index: int) -> str:
    return _QUESTIONS[index]["text"]


def _option_labels(index: int) -> list[str]:
    return [opt["label"] for opt in _QUESTIONS[index]["options"]]


@router.message(F.text == "Пройти тест")
async def start_quiz(message: Message, state: FSMContext) -> None:
    if len(_QUESTIONS) != len(_STATES):
        await message.answer(
            "Тест временно недоступен: число вопросов в данных не совпадает с шагами FSM."
        )
        return

    await state.clear()
    scores = empty_scores()
    await state.update_data(scores=dict(scores), current_q=0)
    await state.set_state(_STATES[0])
    await message.answer(
        "Сейчас будет несколько вопросов. В конце покажу направление по интересам "
        "и идеи кружков и хобби.\n\n"
        f"<b>Вопрос 1 из {len(_QUESTIONS)}</b>\n{_question_text(0)}",
        reply_markup=quiz_options_keyboard(0, _option_labels(0)),
    )


@router.callback_query(
    F.data.startswith("quiz:"),
    StateFilter(
        OrientationStates.question_1,
        OrientationStates.question_2,
        OrientationStates.question_3,
    ),
)
async def on_quiz_answer(callback: CallbackQuery, state: FSMContext) -> None:
    if not callback.data or not callback.message:
        await callback.answer()
        return

    parts = callback.data.split(":")
    if len(parts) != 3:
        await callback.answer()
        return

    try:
        q_idx = int(parts[1])
        opt_idx = int(parts[2])
    except ValueError:
        await callback.answer()
        return

    data = await state.get_data()
    current_q = data.get("current_q", 0)
    if q_idx != current_q:
        await callback.answer("Это уже другой вопрос — ответь на текущий.")
        return

    if q_idx < 0 or q_idx >= len(_QUESTIONS):
        await callback.answer()
        return

    options = _QUESTIONS[q_idx]["options"]
    if opt_idx < 0 or opt_idx >= len(options):
        await callback.answer()
        return

    scores_map = empty_scores()
    scores_map.update(data.get("scores") or {})
    merge_scores(scores_map, options[opt_idx]["scores"])

    await callback.answer()

    if q_idx >= len(_QUESTIONS) - 1:
        await callback.message.edit_reply_markup(reply_markup=None)
        await send_test_outcome_from_callback(callback, dict(scores_map))
        await state.clear()
        return

    next_q = q_idx + 1
    await state.update_data(scores=dict(scores_map), current_q=next_q)
    await state.set_state(_STATES[next_q])
    body = (
        f"<b>Вопрос {next_q + 1} из {len(_QUESTIONS)}</b>\n"
        f"{_question_text(next_q)}"
    )
    await callback.message.edit_text(
        body,
        reply_markup=quiz_options_keyboard(next_q, _option_labels(next_q)),
    )


@router.message(
    StateFilter(
        OrientationStates.question_1,
        OrientationStates.question_2,
        OrientationStates.question_3,
    ),
)
async def quiz_expected_buttons(message: Message) -> None:
    await message.answer(
        "Сейчас нужно выбрать вариант кнопкой под вопросом. "
        "Или нажми «Пройти тест» в меню, чтобы начать заново."
    )
