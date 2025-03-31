from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.models import User
from database.session import Database


class AdminRepository:
    def __init__(self, db: Database):
        self.db = db




# async def get_all_admins(db: AsyncSession):
#     stmt = select(User).where(User.privileges.in_(["Создатель", "Гл. Админ", "Админ", "Модератор"]))
#     result = await db.execute(stmt)
#     return result.scalars().all()
