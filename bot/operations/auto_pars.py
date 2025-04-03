import asyncio

from database.repositories.bot_config_repo import BotConfigRepository
from database.session import db

from parsing.pars_news import ParsNews

current_task = None



class AutoParser:
    def __init__(self, db):
        self.db = db
        self.task = None
        self.running = False


    async def get_interval(self) -> int:
        config = BotConfigRepository(db=self.db)
        return await config.get_interval_auto_pars() * 60


    async def start_parsing(self) -> str | None:
        while self.running:
            try:
                interval = await self.get_interval()
                parser = ParsNews()

                # Здесь вводим наши парсеры
                await parser.parse_kommersant()
                await parser.parse_bloomberg()
                await parser.parse_reuters()

                await asyncio.sleep(interval)
            except Exception as e:
                await asyncio.sleep(10)
                text = f'Ошибка парсера:\n{e}'


    async def start(self) -> str:
        if self.task and not self.task.done():
            return "Парсер уже запущен!"
        self.running = True
        self.task = asyncio.create_task(self.start_parsing())
        return "Парсер запущен!"

    async def stop(self) -> str | None:
        self.running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                return "Парсер остановлен."
            except Exception as e:
                return f"Остановка парсера выдала ошибку:\n{e}"


    async def restart(self):
        await self.stop()
        await self.start()

auto_parser = AutoParser(db)