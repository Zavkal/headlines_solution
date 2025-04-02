import asyncio

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

from database.repositories.news_sources_repo import news_sources_repository


def start_base_panel():
    keyboard = [
        [KeyboardButton(text="📝 Главное меню")],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_start_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🌐 Источники 🌐', callback_data="get_sources_hand")],
        [InlineKeyboardButton(text='💸 Авто получение новостей 💸', callback_data="get_sources_auto")],
        [InlineKeyboardButton(text='🫂 О нас 🫂', callback_data="about_text")],
        [InlineKeyboardButton(text='📔 FAQ - функции бота. 📔', callback_data="faq_text")],
    ])

    return keyboard


def back_base_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'⏪ Назад', callback_data="back_start_menu"),]
        ])

    return keyboard


def sources_menu(sources):
    keyboard = InlineKeyboardMarkup(row_width=2, inline_keyboard=[])

    for source in sources:
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=source["name"],
                callback_data=f"get_headlines_hand:{source['id']}"
            )
        ])


    keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_start_menu")],
    )

    return keyboard























