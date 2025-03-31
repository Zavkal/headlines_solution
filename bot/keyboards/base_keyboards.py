from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup


def start_base_panel():
    keyboard = [
        [KeyboardButton(text="📝 Главное меню")],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_start_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🌐 Источники 🌐', callback_data="")],
        [InlineKeyboardButton(text='💸 Пополнить баланс 💸', callback_data="top_up_balance")],
        [InlineKeyboardButton(text='🫂 О нас 🫂', callback_data="about_text")],
        [InlineKeyboardButton(text='📔 FAQ - функции бота. 📔', callback_data="faq_text")],
    ])

    return keyboard


def withdraw_ref_balance_keyboard(partner: bool = False):
    if partner:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f'💸 Вывести реферальный баланс 💸', callback_data=f"withdraw_ref_balance:{partner}")],
            [InlineKeyboardButton(text=f'⏪ Назад', callback_data="back_start_menu")],
        ])
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f'💸 Вывести реферальный баланс 💸', callback_data=f"withdraw_ref_balance:{partner}")],
            [InlineKeyboardButton(text=f'🧲 Получить вечную реферальную ссылку 🧲', callback_data="all_life_ref_link")],
            [InlineKeyboardButton(text=f'⏪ Назад', callback_data="back_start_menu")],
        ])

    return keyboard


def back_base_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'⏪ Назад', callback_data="back_start_menu"),]
        ])

    return keyboard























