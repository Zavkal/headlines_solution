from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

from config import roles
from database.repositories.admins_repo import admin_repo


def start_admin_panel():
    keyboards = [
        [KeyboardButton(text="📝 Админ панель")],
        [KeyboardButton(text="📝 Главное меню")],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboards, resize_keyboard=True)


def admin_panel_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'🕶 Управление Администраторами', callback_data=f"manage_privileges"),],
        [InlineKeyboardButton(text=f'⚙️ Настройки бота', callback_data=f"edit_bot_config"),],
        [InlineKeyboardButton(text=f'🔐 Выдать бан клиенту', callback_data=f"get_ban_user"), ],
        [InlineKeyboardButton(text=f'🔓 Выдать разблокировку клиенту', callback_data=f"get_unban_user"), ],
        ])

    return keyboard


async def get_admin_management_keyboard():
    admins = await admin_repo.get_all_admins()

    keyboard = InlineKeyboardMarkup(row_width=2, inline_keyboard=[])

    for admin in admins:
        keyboard.inline_keyboard.append([InlineKeyboardButton(
            text=f"{admin['telegram_id']} - {admin['username']} ({admin['privilege']})",
            callback_data=f"manage_admin:{admin['telegram_id']}"
        )])

    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="➕ Добавить роль", callback_data="add_privilege"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="back_admin_panel_callback")
    ])

    return keyboard


def add_privilege_keyboard(user_id: int):
    keyboard = InlineKeyboardMarkup(row_width=2, inline_keyboard=[])

    for role in roles:
        if role != 'users':
            keyboard.inline_keyboard.append([InlineKeyboardButton(
                text=role,
                callback_data=f"set_role:{user_id}:{role}"
            )])

    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="🔙 Назад", callback_data="manage_privileges")
    ])

    return keyboard


def manage_admin_keyboard(user_id: int):
    keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[])
    inline_buttons = []

    inline_buttons.append(
        InlineKeyboardButton(text="✏ Изменить роль", callback_data=f"change_role:{user_id}")
    )
    inline_buttons.append(
        InlineKeyboardButton(text="🗑 Удалить", callback_data=f"remove_admin:{user_id}")
    )
    inline_buttons.append(
        InlineKeyboardButton(text="🔙 Назад", callback_data="manage_privileges")
    )

    keyboard.inline_keyboard = [inline_buttons]

    return keyboard


def change_role_keyboard(user_id: int):
    keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[])
    inline_buttons = []
    for role in roles:
        inline_buttons.append(InlineKeyboardButton(text=role, callback_data=f"set_role:{user_id}:{role}"))

    inline_buttons.append(InlineKeyboardButton(text="🔙 Назад", callback_data="manage_privileges"))
    keyboard.inline_keyboard = [inline_buttons]
    return keyboard


def edit_bot_description_about_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'Перезапустить парсер', callback_data=f"restart_parser"),],
        [InlineKeyboardButton(text=f'Изменить таймер автопарсинга', callback_data=f"edit_bot_description"),],
        [InlineKeyboardButton(text=f'Задать текст бота (гл.Меню)', callback_data=f"edit_bot_about"),],
        [InlineKeyboardButton(text=f'Задать описание бота (FAQ)', callback_data=f"edit_bot_faq"),],
        [InlineKeyboardButton(text=f'💬 Отправить сообщение всем', callback_data=f"all_send_message"),],
        [InlineKeyboardButton(text=f'🔙Назад', callback_data=f"back_admin_panel_callback"),],
        ])
    return keyboard


def delete_message_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'⛔️ Отменить отправку', callback_data=f"delete_message:"),],
        ])

    return keyboard




