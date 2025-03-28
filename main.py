import asyncio

from bot.config import dp, bot

async def main():
    dp.include_routers(
                      )
    print("Бот запущен")
    await dp.start_polling(bot, skip_updates=True)


# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())