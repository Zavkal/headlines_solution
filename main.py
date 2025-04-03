import asyncio

from bot.config import dp, bot
from bot.handlers.start_handler import router as start_handler
from bot.handlers.base_handler import router as base_handler
from bot.handlers.headlines_handler import router as headlines_handler
from bot.handlers.admin_handler import router as admin_handler
from bot.logger import logger
from bot.operations.auto_pars import auto_parser


async def main():
    await auto_parser.start()
    dp.include_routers(
        start_handler,
        base_handler,
        headlines_handler,
        admin_handler,
                      )
    logger.info("Бот запущен")
    await dp.start_polling(bot, skip_updates=True)


# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())