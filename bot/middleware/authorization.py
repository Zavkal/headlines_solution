from functools import wraps
from aiogram import types

from bot.config import creator_id
from database.repositories.users_repo import users_repo



async def get_user_role(telegram_id: int) -> str | None:
    status_ban = await users_repo.is_user_banned(telegram_id)
    privileges = await users_repo.get_privileges(telegram_id)

    return status_ban if status_ban else privileges


def authorization(required_roles: list[str]):
    """
    Декоратор для проверки прав доступа.

    :param required_roles: Список ролей, которым разрешён доступ.
    """

    def decorator(func):
        @wraps(func)
        async def wrapped(callback_query: types.CallbackQuery, *args, **kwargs):
            telegram_id = callback_query.from_user.id

            if telegram_id == creator_id: # gl.admin
                role = 'creator'
            else:
                role = await get_user_role(telegram_id)

            if role in required_roles:
                return await func(callback_query, *args, **kwargs)

        return wrapped

    return decorator


# @authorization(["creator", "administrator", "users"])



