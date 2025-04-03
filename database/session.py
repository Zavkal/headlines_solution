from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from bot.config import DATABASE_URL
from database.Base import Base


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


db = Database(DATABASE_URL)
