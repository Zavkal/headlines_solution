from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.repositories.news_sources_repo import news_sources_repository
from database.repositories.source_subscriptions_repo import sources_subscriptions


async def sources_menu():
    sources = await news_sources_repository.get_all_source()
    keyboard = InlineKeyboardMarkup(row_width=2, inline_keyboard=[])

    for source in sources:
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=source["name"],
                callback_data=f"get_headlines_hand:{source['id']}:{source['name']}"
            )
        ])


    keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_start_menu")],
    )

    return keyboard


async def sources_menu_auto(telegram_id: int):
    sources = await news_sources_repository.get_all_source()
    keyboard = InlineKeyboardMarkup(row_width=2, inline_keyboard=[])
    for source in sources:
        is_subscribed = await sources_subscriptions.is_subscription(telegram_id=telegram_id,
                                                                    source_id=source.get('id'))
        emoji = "✅" if is_subscribed else "❌"
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=f'{emoji} - {source["name"]}',
                callback_data=f"del_or_add_subscription:{source['id']}:{is_subscribed}"
            )
        ])


    keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_start_menu")],
    )

    return keyboard
