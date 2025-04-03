from sqlalchemy.future import select
from database.models import User
from database.session import Database, db


class UserRepository:
    def __init__(self, db: Database):
        self.db = db


    async def create_user(self, telegram_id: int, username: str) -> User:
        async with self.db.session() as session:
            result = await session.execute(select(User).filter_by(telegram_id=telegram_id))
            existing_user = result.scalar_one_or_none()  # Получаем первого пользователя или None, если нет

            if existing_user:  # Если пользователь существует, возвращаем его
                return existing_user

            user = User(telegram_id=telegram_id, username=username)
            session.add(user)
            await session.commit()
            return user


    async def user_in_db(self, telegram_id: int) -> bool | None:
        async with self.db.session() as session:
            result = await session.execute(select(User).where(User.telegram_id == telegram_id))
            result = result.scalar()
            if result:
                return True


    async def get_all_users(self) -> list[int]:
        async with self.db.session() as session:
            result = await session.execute(select(User.telegram_id))  # Запрашиваем только нужный столбец
            return result.scalars().all()


    async def update_user(self, telegram_id: int, **kwargs) -> User | None:
        async with self.db.session() as session:
            result = await session.execute(select(User).where(User.telegram_id == telegram_id))
            user = result.scalar()
            if user:
                for key, value in kwargs.items():
                    setattr(user, key, value)
                    await session.commit()
                    return user
            return None


    async def delete_user(self, telegram_id: int) -> User | None:
        async with self.db.session() as session:
            result = await session.execute(select(User).where(User.telegram_id == telegram_id))
            user = result.scalar()
            if user:
                await session.delete(user)
                await session.commit()
                return user
            return None


    async def is_user_banned(self, telegram_id: int) -> bool | None:
        async with self.db.session() as session:
            result = await session.execute(select(User).where(User.telegram_id == telegram_id))
            user = result.scalar()
            return user.is_banned if user else None


    async def get_privileges(self, telegram_id: int) -> str:
        async with self.db.session() as session:
            result = await session.execute(select(User).where(User.telegram_id == telegram_id))
            user = result.scalar()
            return user.privileges if user else None


    async def set_status_ban_users(self, telegram_id: int, new_status: bool) -> None:
        async with self.db.session() as session:
            query = select(User).where(User.telegram_id == telegram_id)
            result = await session.execute(query)
            user = result.scalars().first()
            if user:
                user.is_banned = new_status
                await session.commit()


users_repo = UserRepository(db)












