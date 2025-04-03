from sqlalchemy.future import select
from database.models import NewsSource, NewsHeadline
from database.session import Database, db


class NewsSourcesRepository:
    def __init__(self, db: Database):
        self.db = db

    async def get_source_id(self, url: str) -> int:
        async with self.db.session() as session:
            source = await session.execute(select(NewsSource).filter_by(url=url))
            source = source.scalar()
            if source is None:
                raise ValueError('Source does not exist')


            return source.id


    async def get_all_source(self) -> list[dict[str, str]]:
        async with self.db.session() as session:
            source = await session.execute(select(NewsSource))
            sources = source.scalars().all()
            return [s.__dict__ for s in sources]


    async def get_source_url(self, source_id) -> str:
        async with self.db.session() as session:
            source = await session.execute(select(NewsSource).filter_by(id=source_id))
            result = source.scalar()
            return result.url




news_sources_repository = NewsSourcesRepository(db)