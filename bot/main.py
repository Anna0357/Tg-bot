import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramNetworkError
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import Config, load_config
from bot.handlers import router

log = logging.getLogger(__name__)


def _build_session(config: Config) -> AiohttpSession:
    kwargs: dict = {"timeout": config.request_timeout}
    if config.telegram_proxy:
        kwargs["proxy"] = config.telegram_proxy
    return AiohttpSession(**kwargs)


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    config = load_config()
    if config.telegram_proxy:
        log.info("Используется прокси для Telegram API (TELEGRAM_PROXY)")
    log.info("Таймаут запросов к API: %s с", config.request_timeout)

    bot = Bot(
        token=config.bot_token,
        session=_build_session(config),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    try:
        await dp.start_polling(bot)
    except TelegramNetworkError as exc:
        log.error(
            "Нет связи с Telegram API (%s). Включите VPN или укажите в .env "
            "TELEGRAM_PROXY (HTTP/HTTPS/SOCKS5), проверьте файрвол и DNS.",
            exc,
        )
        raise SystemExit(1) from exc
