from datetime import datetime

from sqlalchemy.future import select
from database.models import NewsHeadline
from database.session import Database, db


class HeadlinesRepository:
    def __init__(self, db: Database):
        self.db = db


    async def create_news(self,
                          url: str,
                          date_published: datetime,
                          title: str,
                          category: str,
                          source_id: int) -> bool:
        async with self.db.session() as session:
            result = await session.execute(select(NewsHeadline).filter_by(url=url))
            existing_headlines = result.scalar_one_or_none()

            if existing_headlines:
                return False

            headlines = NewsHeadline(url=url,
                                     date_published=date_published,
                                     title=title,
                                     category=category,
                                     source_id=source_id,
                                     )
            session.add(headlines)
            await session.commit()
            return True


    async def get_news(self, source_id: int, counter: int) -> list[NewsHeadline]:
        async with self.db.session() as session:
            result = await session.execute(
                select(NewsHeadline).filter_by(source_id=source_id).order_by(NewsHeadline.id.desc()).limit(counter)
            )
            return result.scalars().all()


headlines_repo = HeadlinesRepository(db)