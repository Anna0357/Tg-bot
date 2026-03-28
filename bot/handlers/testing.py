from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.handlers.results import send_test_outcome_from_callback
from bot.keyboards.inline import quiz_options_keyboard
from bot.services.scoring import empty_scores, load_quiz, merge_scores
from bot.states.orientation import OrientationStates

router = Router(name="testing")

_QUESTIONS = load_quiz()
_OPTION_LETTERS = ("А", "Б", "В", "Г")


def _question_text(index: int) -> str:
    return _QUESTIONS[index]["text"]


def _option_labels(index: int) -> list[str]:
    return [opt["label"] for opt in _QUESTIONS[index]["options"]]


def _question_message_block(index: int) -> str:
    lines = [
        f"<b>Вопрос {index + 1} из {len(_QUESTIONS)}</b>",
        _question_text(index),
        "",
    ]
    for letter, label in zip(_OPTION_LETTERS, _option_labels(index)):
        lines.append(f"{letter}) {label}")
    return "\n".join(lines)


@router.message(F.text == "Пройти тест")
async def start_quiz(message: Message, state: FSMContext) -> None:
    if not _QUESTIONS:
        await message.answer("Тест временно недоступен: нет вопросов в данных.")
        return

    await state.clear()
    scores = empty_scores()
    await state.update_data(scores=dict(scores), current_q=0)
    await state.set_state(OrientationStates.taking_quiz)
    n_opts = len(_QUESTIONS[0]["options"])
    await message.answer(
        "Сейчас — опросник по методике Йовайши (модификация Резапкиной): "
        "24 вопроса, в каждом выбери <b>один</b> вариант — А, Б или В.\n\n"
        "В конце покажу сферы профессиональных склонностей (I–VI) и идеи кружков и хобби.\n\n"
        f"{_question_message_block(0)}",
        reply_markup=quiz_options_keyboard(0, n_opts),
    )


@router.callback_query(F.data.startswith("quiz:"), StateFilter(OrientationStates.taking_quiz))
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
    n_opts = len(_QUESTIONS[next_q]["options"])
    await callback.message.edit_text(
        _question_message_block(next_q),
        reply_markup=quiz_options_keyboard(next_q, n_opts),
    )


@router.message(StateFilter(OrientationStates.taking_quiz))
async def quiz_expected_buttons(message: Message) -> None:
    await message.answer(
        "Сейчас нужно выбрать вариант кнопкой А, Б или В под вопросом. "
        "Или нажми «Пройти тест» в меню, чтобы начать заново."
    )
