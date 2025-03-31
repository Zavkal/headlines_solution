# from database.repositories.admins_repo import get_all_admins
# from database.session import get_async_session
#
#
# async def is_admin(telegram_id: int):
#     async with get_async_session() as session:
#         admins = await get_all_admins(session)
#         print(admins)
#         for admin in admins:
#             print(f"Admin: {admin.username} ({admin.privileges})")
