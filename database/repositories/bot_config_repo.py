from sqlalchemy.future import select

from database.models import BotConfig
from database.session import Database, db


class BotConfigRepository:
    def __init__(self, db: Database):
        self.db = db


    async def get_interval_auto_pars(self) -> int:
        async with self.db.session() as session:
            config = await session.execute(select(BotConfig))
            config = config.scalars().first()

            return config.auto_parse_interval


    async def get_about_text(self) -> str:
        async with self.db.session() as session:
            config = await session.execute(select(BotConfig))
            config = config.scalars().first()
            return config.about_text


    async def get_faq_text(self) -> str:
        async with self.db.session() as session:
            config = await session.execute(select(BotConfig))
            config = config.scalars().first()
            return config.faq_text


    async def edit_about_text(self, text: str) -> None:
        async with self.db.session() as session:
            config = await session.get(BotConfig, 1)  # Получаем запись с ID = 1
            if config:
                config.about_text_config = text
                await session.commit()


    async def edit_faq_text(self, text: str) -> None:
        async with self.db.session() as session:
            config = await session.get(BotConfig, 1)  # Получаем запись с ID = 1
            if config:
                config.faq_text_config = text
                await session.commit()




bot_config = BotConfig(db)



