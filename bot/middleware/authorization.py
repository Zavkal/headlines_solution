# from functools import wraps
# from aiogram import types
#
#
#
# def get_user_role(telegram_id: int) -> str | None:
#     users = '' # Дать юзера
#     admin = '' # Дать админа
#
#     if customer:
#         if customer.get('ban') == 1:
#             return None
#         elif customer.get('telegram_id') == 1637636761:
#             return 'creator'
#         else:
#             if admin_role:
#                 return admin_role.get('role')
#             elif customer:
#                 return 'users' if customer.get('ban') == 0 else 'banned'
#         return None
#     else:
#         return 'users'
#
#
# def authorization(required_roles: list[str]):
#     """
#     Декоратор для проверки прав доступа.
#
#     :param required_roles: Список ролей, которым разрешён доступ.
#     """
#
#     def decorator(func):
#         @wraps(func)
#         async def wrapped(callback_query: types.CallbackQuery, *args, **kwargs):
#             telegram_id = callback_query.from_user.id
#             role = get_user_role(telegram_id)
#
#             if role in required_roles:
#                 return await func(callback_query, *args, **kwargs)
#
#         return wrapped
#
#     return decorator
#
#
# # @authorization(["creator", "administrator", "users"])
#
#
#
