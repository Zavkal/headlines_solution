from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup



def start_admin_panel(telegram_id: int):
    keyboards = [
        [KeyboardButton(text="🔓 Включить смену")],
        [KeyboardButton(text="📝 Админ панель")],
        [KeyboardButton(text="📝 Главное меню")],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboards, resize_keyboard=True)


# def get_admin_management_keyboard(telegram_id):
#     admins = get_all_admins()
#
#     # Инициализация клавиатуры
#     keyboard = InlineKeyboardMarkup(row_width=2, inline_keyboard=[])
#
#     # Формируем кнопки для админов
#     inline_buttons = []
#     for admin in admins:
#         if admin['role'] != 'creator' or telegram_id != admin['telegram_id']:  # Исключаем создателя
#             inline_buttons.append(InlineKeyboardButton(
#                 text=f"{admin['telegram_id']} - {admin['username']} ({admin['role']})",
#                 callback_data=f"manage_admin:{admin['telegram_id']}"
#             ))
#
#     # Разбиваем список на ряды по 2 кнопки
#     for i in range(0, len(inline_buttons), 2):
#         keyboard.inline_keyboard.append(inline_buttons[i:i+2])
#
#     # Добавляем кнопки "Добавить роль" и "Назад" на отдельную строку
#     keyboard.inline_keyboard.append([
#         InlineKeyboardButton(text="➕ Добавить роль", callback_data="add_privilege"),
#         InlineKeyboardButton(text="🔙 Назад", callback_data="back_admin_panel_callback")
#     ])
#
#     return keyboard


def admin_panel_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'🕶 Управление Администраторами', callback_data=f"manage_privileges"),],
        [InlineKeyboardButton(text=f'🧑‍🏭 Управление воркерами', callback_data=f"manage_workers"),],
        [InlineKeyboardButton(text=f'🧍 Управление партнерами', callback_data=f"callback_give_kb_partners"),],
        [InlineKeyboardButton(text=f'📊 Статистика', callback_data=f"callback_give_kb_statistic"),],
        [InlineKeyboardButton(text=f'⚙️ Изменить настройки бота', callback_data=f"edit_bot_config"),],
        [InlineKeyboardButton(text=f'💬 Получить весь диалог по номеру заказа', callback_data=f"get_all_message_order"),],
        [InlineKeyboardButton(text=f'🔐 Выдать бан клиенту', callback_data=f"get_ban_customer"), ],
        [InlineKeyboardButton(text=f'Выдать разблокировку клиенту', callback_data=f"get_unban_customer"), ],
        [InlineKeyboardButton(text=f'🚩 Активные тикеты', callback_data=f"get_all_active_ticket"),],
        [InlineKeyboardButton(text=f'💸 Заявки на вывод', callback_data=f"withdraw_balance_worker"),],
        ])

    return keyboard


def client_admin_worker_keyboard(order_id: int, ticket_id: int):
    if order_id:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f'💬 Написать клиенту', callback_data=f"send_client_worker_message:{ticket_id}:{order_id}:client"),],
            [InlineKeyboardButton(text=f'💬 Написать воркеру', callback_data=f"send_client_worker_message:{ticket_id}:{order_id}:worker"),],
            [InlineKeyboardButton(text=f'Закрыть заказ в пользу покупателя', callback_data=f"close_ticket:{ticket_id}:{order_id}:client"),],
            [InlineKeyboardButton(text=f'Закрыть заказ в пользу воркера', callback_data=f"close_ticket:{ticket_id}:{order_id}"),],
            ])
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f'💬 Написать клиенту', callback_data=f"send_client_worker_message:{ticket_id}:client"),],
            [InlineKeyboardButton(text=f'Закрыть тикет', callback_data=f"close_ticket:{ticket_id}:client"),],
            ])

    return keyboard


def resend_message_keyboard(telegram_id, ticket_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'💬 Ответить', callback_data=f"resend_message:{telegram_id}:{ticket_id}"),],
        ])

    return keyboard


def edit_bot_description_about_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'Изменить цены подписей', callback_data=f"change_price_signature"),],
        [InlineKeyboardButton(text=f'Изменить сообщение в гл.меню', callback_data=f"edit_bot_description"),],
        [InlineKeyboardButton(text=f'Изменить сообщение "О нас', callback_data=f"edit_bot_about"),],
        [InlineKeyboardButton(text=f'💬 Отправить сообщение всем', callback_data=f"all_send_message"),],
        [InlineKeyboardButton(text=f'Назад', callback_data=f"back_admin_panel_callback"),],
        ])

    return keyboard


def statistic_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'Статистика пополнений', callback_data=f"statistic_top_up"),],
        [InlineKeyboardButton(text=f'Статистика заказов', callback_data=f"statistic_orders"),],
        [InlineKeyboardButton(text=f'Общая статистика файлом', callback_data=f"statistic_in_document"),],
        ])

    return keyboard



