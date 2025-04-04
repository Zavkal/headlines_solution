from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select

from bot.config import DATABASE_URL
from database.Base import Base
from database.models import BotConfig, NewsSource


class Database:
    """Класс для управления подключением к базе данных."""

    _instance = None

    def __new__(cls, db_url: str = DATABASE_URL):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._init(db_url)
        return cls._instance

    def _init(self, db_url: str) -> None:
        """Инициализация подключения"""
        self._engine = create_async_engine(db_url, echo=False)
        self._async_session = async_sessionmaker(
            self._engine,
            expire_on_commit=False
        )


    async def create_database(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


    @asynccontextmanager
    async def session(self) -> AsyncSession:
        """Контекстный менеджер для безопасной работы с сессией."""
        async_session = self._async_session()
        try:
            yield async_session
            await async_session.commit()
        except Exception:
            await async_session.rollback()
            raise
        finally:
            await async_session.close()


    async def get_session(self) -> AsyncSession:
        return self._async_session()


    async def seed_data(self):
        async with self.session() as session:
            config_exists = await session.execute(select(BotConfig))
            if not config_exists.scalars().first():
                session.add(BotConfig())  # все дефолтное

            sources_exists = await session.execute(select(NewsSource))
            if not sources_exists.scalars().first():
                session.add_all([
                    NewsSource(name="Bloomberg", url="https://www.bloomberg.com"),
                    NewsSource(name="Reuters", url="https://www.reuters.com"),
                    NewsSource(name="Коммерсант", url="https://www.kommersant.ru"),
                ])



db = Database(DATABASE_URL)
