from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.models import User
from database.session import Database, db


class AdminRepository:
    def __init__(self, db: Database):
        self.db = db


    async def get_all_admins(self) -> list[dict]:
        async with self.db.session() as session:
            query = select(User).where(User.privileges.in_(["administrator"]))
            result = await session.execute(query)
            admins = result.scalars().all()
            all_admins = []
            for admin in admins:
                all_admins.append({
                    'telegram_id': admin.telegram_id,
                    'username': admin.username,
                    'privilege': admin.privileges,
                })
            return all_admins


    async def edit_privilege(self, telegram_id: int, new_privilege: str) -> None:
        async with self.db.session() as session:
            query = select(User).where(User.telegram_id == telegram_id)
            result = await session.execute(query)
            user = result.scalars().first()

            if not user:
                return None

            user.privileges = new_privilege
            await session.commit()



admin_repo = AdminRepository(db)