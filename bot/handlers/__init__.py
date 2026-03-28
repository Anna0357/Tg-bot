from aiogram import Router

from bot.handlers import intro, menu, testing

router = Router()
router.include_router(intro.router)
router.include_router(menu.router)
router.include_router(testing.router)

__all__ = ["router"]
