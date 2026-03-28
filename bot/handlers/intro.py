from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from bot.keyboards.reply import main_menu_keyboard

router = Router(name="intro")


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    text = (
        "Привет! Я бот профориентации для подростков.\n\n"
        "<b>Как это работает</b>\n"
        "1) Ты проходишь короткий тест.\n"
        "2) По ответам подбирается направление (тип профессиональных интересов).\n"
        "3) Я предложу идеи кружков и хобби, которые помогают развить это направление.\n\n"
        "Тест и подсказки можно менять без переписывания кода — вопросы и правила лежат в "
        "файлах <code>bot/data/</code>.\n\n"
        "Решение о будущей профессии всегда за тобой; бот лишь помогает сориентироваться.\n\n"
        "Выбери действие в меню ниже."
    )
    await message.answer(text, reply_markup=main_menu_keyboard())


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(
        "<b>Команды</b>\n"
        "/start — приветствие и меню\n"
        "/help — эта подсказка\n\n"
        "<b>Меню</b>\n"
        "Пройти тест — профориентационный опрос\n"
        "О профессиях — кратко о направлениях\n"
        "Полезные ссылки — куда ещё заглянуть",
        reply_markup=main_menu_keyboard(),
    )
