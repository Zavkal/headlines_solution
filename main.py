import asyncio

from config import dp, bot
from bot.handlers.start_handler import router as start_handler
from bot.handlers.base_handler import router as base_handler
from database.session import db


async def main():
    dp.include_routers(
        start_handler,
        base_handler,
                      )
    print("Бот запущен")
    await dp.start_polling(bot, skip_updates=True)


# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())