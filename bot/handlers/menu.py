from aiogram import F, Router
from aiogram.types import Message

from bot.keyboards.reply import main_menu_keyboard
from bot.services.scoring import load_professions

router = Router(name="menu")


@router.message(F.text == "О профессиях")
async def show_professions(message: Message) -> None:
    by_id = load_professions()
    chunks = ["Кратко о направлениях (после теста будет персональнее):\n"]
    for info in by_id.values():
        chunks.append(f"\n<b>{info['title']}</b>\n{info['description']}")
    await message.answer("\n".join(chunks), reply_markup=main_menu_keyboard())


@router.message(F.text == "Полезные ссылки")
async def useful_links(message: Message) -> None:
    text = (
        "<b>Полезные ресурсы</b>\n"
        "• Официальные порталы про профессии и образование в РФ — по запросу "
        "«профессии» и региону.\n"
        "• Школьный сайт и районный методкабинет: кружки, олимпиады, дни открытых дверей.\n"
        "• Классный руководитель и профориентолог школы — про локальные программы и практику."
    )
    await message.answer(text, reply_markup=main_menu_keyboard())
