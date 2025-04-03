import asyncio

from bot.config import bot
from bot.logger import logger
from bot.operations.generate_text_headlines import generate_text
from database.repositories.bot_config_repo import BotConfigRepository
from database.repositories.headlines_repo import HeadlinesRepository, headlines_repo
from database.repositories.news_sources_repo import news_sources_repository
from database.repositories.source_subscriptions_repo import sources_subscriptions
from database.session import db

from parsing.pars_news import ParsNews

current_task = None



class AutoParser:
    def __init__(self, db):
        self.db = db
        self.task = None
        self.running = False
        self.new_links = []
        self.parser = ParsNews()


    async def get_interval(self) -> int:
        config = BotConfigRepository(db=self.db)
        return await config.get_interval_auto_pars() * 60


    async def collect_new_links(self, links: list) -> None:
        for link in links:
            if not await headlines_repo.link_exists(link):  # Если ссылка новая
                self.new_links.append(link)


    async def start_parsing(self) -> str | None:
        while self.running:
            try:
                interval = await self.get_interval()
                links_to_send = []

                # Здесь вводим наши парсеры
                new_links = await self.parser.parse_kommersant()
                links_to_send.extend(new_links)

                new_links = await self.parser.parse_bloomberg()
                links_to_send.extend(new_links)

                new_links = await self.parser.parse_reuters()
                links_to_send.extend(new_links)


                links_to_send.extend(self.new_links)
                await self.send_links_to_users(links_to_send)

                await asyncio.sleep(interval)
            except Exception as e:
                logger.exception(e)
                await asyncio.sleep(10)
                logger.exception(f'Ошибка парсера:\n{e}')


    async def start(self) -> None:
        if self.task and not self.task.done():
            logger.exception("Парсер уже запущен!")
        self.running = True
        self.task = asyncio.create_task(self.start_parsing())
        logger.info("Парсер запущен!")

    async def stop(self) -> str | None:
        self.running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                logger.info("Парсер остановлен.")
            except Exception as e:
                logger.exception(f"Остановка парсера выдала ошибку:\n{e}")


    async def restart(self):
        await self.stop()
        await self.start()


    @staticmethod
    async def send_links_to_users(headlines: list):
        all_subscriptions = await sources_subscriptions.get_users_and_subscriptions()
        source_name = await news_sources_repository.get_dict_source_name_by_id()
        for headline in headlines:
            if headline:
                for user_subscription in all_subscriptions:
                    if headline.source_id in user_subscription.get('source_id'):
                        try:
                            await bot.send_message(chat_id=user_subscription.get('telegram_id'),
                                                   text=await generate_text(headline=headline, source_name=source_name.get(headline.source_id)),
                                                    parse_mode="HTML",
                                                   disable_web_page_preview=True)
                        except Exception as e:
                            logger.exception(e)


auto_parser = AutoParser(db)