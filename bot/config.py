import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    bot_token: str


def load_config() -> Config:
    token = (os.getenv("BOT_TOKEN") or "").strip()
    if not token:
        msg = "Задайте BOT_TOKEN в переменных окружения или в файле .env"
        raise ValueError(msg)
    return Config(bot_token=token)
