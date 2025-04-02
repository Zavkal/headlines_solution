from aiogram import Bot, Dispatcher
import os

from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())

DATABASE_URL = (f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
                f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")





category_kommersnat = {
    '2': 'politics',
    '3': 'economy',
    '4': 'business',
    '5': 'world',
    '6': 'incident',
    '7': 'society',
    '8': 'culture',
    '9': 'sport',
}