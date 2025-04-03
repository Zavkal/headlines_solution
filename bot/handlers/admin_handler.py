import asyncio

from aiogram import types, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile, FSInputFile
from aiogram.types import CallbackQuery, Union

from bot.keyboards.admin_keyboards import get_admin_management_keyboard, admin_panel_keyboard, manage_admin_keyboard, \
    change_role_keyboard, delete_message_keyboard, edit_bot_description_about_keyboard, add_privilege_keyboard
from bot.middleware.authorization import authorization
from bot.operations.auto_pars import auto_parser
from config import roles
from database.repositories.admins_repo import admin_repo
from database.repositories.bot_config_repo import bot_config
from database.repositories.users_repo import users_repo

router = Router(name="Администраторы")

class NewMessageForAll(StatesGroup):
    waiting_message = State()

class GetBanCostumer(StatesGroup):
    waiting_costumer_id = State()

class NewFaqBot(StatesGroup):
    waiting_description = State()

class NewAboutBot(StatesGroup):
    waiting_about = State()


class PrivilegeManagement(StatesGroup):
    waiting_telegram_id = State()


@router.message(F.text == "📝 Админ панель")
@router.callback_query(F.data == 'back_admin_panel_callback')
@authorization(["creator", "administrator"])
async def admin_panel_handler(event: Union[types.Message, CallbackQuery], state: FSMContext, ) -> None:
    await state.clear()
    await event.bot.send_message(chat_id=event.from_user.id,
                                 text='Добро пожаловать.',
                                 reply_markup=admin_panel_keyboard())
    try:
        await event.bot.delete_message(chat_id=event.from_user.id,
                                       message_id=event.message.message_id)
    except:
        await event.delete()




@router.callback_query(F.data == 'manage_privileges')
@authorization(["creator", "administrator"])
async def manage_privileges(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите пользователя для управления:",
                                     reply_markup=await get_admin_management_keyboard())


@router.callback_query(F.data == 'add_privilege')
@authorization(["creator"])
async def add_privilege(callback: types.CallbackQuery, state: FSMContext):
    msg_del = await callback.message.answer(text="Введите Telegram ID пользователя:",
                                            reply_markup=delete_message_keyboard(),
                                            )
    await state.update_data(msg_del=msg_del)
    await state.set_state(PrivilegeManagement.waiting_telegram_id)
    await callback.answer()


@router.message(PrivilegeManagement.waiting_telegram_id)
async def add_privilege_state(message: types.Message, state: FSMContext):
    data = await state.get_data()
    msg_del = data['msg_del']
    try:
        user_id = int(message.text)
        await msg_del.edit_text(text=f'Выберите роль для: {user_id}',
                             reply_markup=add_privilege_keyboard(user_id=user_id),
                             )

    except ValueError:
        mes_del = await message.answer('Ввести можно только цифры!')
        await asyncio.sleep(2)
        await mes_del.delete()
        await message.delete()


@router.callback_query(F.data.startswith("manage_admin:"))
@authorization(["creator", "administrator"])
async def manage_admin(callback: types.CallbackQuery):
    user_id = int(callback.data.split(":")[1])
    await callback.message.edit_text(f"Выберите действие для {user_id}:", reply_markup=manage_admin_keyboard(user_id))
    await callback.answer()


@router.callback_query(F.data.startswith("change_role:"))
@authorization(["creator", "administrator"])
async def change_role(callback: types.CallbackQuery):
    user_id = int(callback.data.split(":")[1])
    await callback.message.edit_text("Выберите новую роль:", reply_markup=change_role_keyboard(user_id))
    await callback.answer()


@router.callback_query(F.data.startswith("set_role:"))
@authorization(["creator", "administrator"])
async def set_role(callback: types.CallbackQuery):
    _, user_id, new_privilege = callback.data.split(":")
    user_id = int(user_id)
    await admin_repo.edit_privilege(telegram_id=user_id, new_privilege=new_privilege)

    await callback.message.edit_text(f"Роль пользователя {user_id} изменена на {new_privilege}.",
                                     reply_markup=await get_admin_management_keyboard())
    await callback.answer()


@router.callback_query(F.data.startswith("remove_admin:"))
@authorization(["creator", "administrator"])
async def remove_admin_handler(callback: types.CallbackQuery):
    user_id = int(callback.data.split(":")[1])

    await admin_repo.edit_privilege(telegram_id=user_id, new_privilege='users')

    await callback.message.edit_text(f"Пользователь {user_id} удалён из администраторов.",
                                     reply_markup=await get_admin_management_keyboard())
    await callback.answer()


@router.callback_query(F.data == "get_ban_user")
@authorization(["creator", "administrator"])
async def get_ban_user_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    mess_del = await callback.message.answer('Введите id пользователя для выдачи бана:',
                                             reply_markup=delete_message_keyboard())
    await state.update_data(mess_del=mess_del, callback=callback, status='ban')
    await state.set_state(GetBanCostumer.waiting_costumer_id)


@router.callback_query(F.data == "get_unban_user")
@authorization(["creator", "administrator"])
async def get_unban_user_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    mess_del = await callback.message.answer('Введите id пользователя для выдачи разбана:',
                                             reply_markup=delete_message_keyboard())
    await state.update_data(mess_del=mess_del, callback=callback, status='unban')
    await state.set_state(GetBanCostumer.waiting_costumer_id)


@router.message(GetBanCostumer.waiting_costumer_id)
async def get_ban_unban_user_state(message: types.Message, state: FSMContext):
    data = await state.get_data()
    mess_del = data.get('mess_del')
    status = data.get('status')

    try:
        telegram_id = int(message.text)
        user = await users_repo.user_in_db(telegram_id)
        if status == 'ban':
            if user:
                await users_repo.set_status_ban_users(telegram_id=telegram_id, new_status=True)
                await message.answer(f'Пользователь {telegram_id} заблокирован.')
            else:
                msg = await message.answer('Данного пользователя нет в базе.')
                await asyncio.sleep(2)
                await msg.delete()
        elif status == 'unban':
            if user:
                await users_repo.set_status_ban_users(telegram_id=telegram_id, new_status=False)
                await message.answer(f'Пользователь {telegram_id} разблокирован.')
            else:
                msg = await message.answer('Данного пользователя нет в базе.')
                await asyncio.sleep(2)
                await msg.delete()

        await mess_del.delete()
        await state.clear()
    except Exception as e:
        print(e)
        msg = await message.answer('Введите id пользователя и ничего более.')
        await asyncio.sleep(2)
        await msg.delete()



@router.callback_query(F.data == "edit_bot_config")
@authorization(["creator", "administrator"])
async def edit_bot_description_about(callback: types.CallbackQuery, state: FSMContext):
    status = auto_parser.running
    await callback.message.edit_text(text=f'Статус парсера: {status}',
                                     reply_markup=edit_bot_description_about_keyboard())


@router.callback_query(F.data == "edit_bot_faq")
@authorization(["creator", "administrator"])
async def edit_bot_description(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    mess_del = await callback.message.answer('Введите новое описание гл.меню бота:',
                                             reply_markup=delete_message_keyboard())
    await state.update_data(mess_del=mess_del, callback=callback)
    await state.set_state(NewFaqBot.waiting_description)


@router.message(NewFaqBot.waiting_description)
async def edit_bot_description_state(message: types.Message, state: FSMContext):
    data = await state.get_data()
    mess_del = data.get('mess_del')
    await bot_config.edit_faq_text(text=message.text)
    await message.answer('Изменения успешно применены')

    await message.delete()
    await mess_del.delete()
    await state.clear()


@router.callback_query(F.data == "edit_bot_about")
@authorization(["creator", "administrator"])
async def edit_bot_about(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    mess_del = await callback.message.answer('Введите новое "О нас" бота:',
                                             reply_markup=delete_message_keyboard())
    await state.update_data(mess_del=mess_del)
    await state.set_state(NewAboutBot.waiting_about)


@router.message(NewAboutBot.waiting_about)
async def edit_bot_about_state(message: types.Message, state: FSMContext):
    data = await state.get_data()
    mess_del = data.get('mess_del')
    await bot_config.edit_about_text(text=message.text)
    await message.answer('Изменения успешно применены')
    await message.delete()
    await mess_del.delete()
    await state.clear()



@router.callback_query(F.data == 'all_send_message')
@authorization(["creator", "administrator"])
async def all_send_message(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    mess_del = await callback.message.answer(text='Введите текст, который необходимо отправить абсолютно всем пользователям!\n'
                                       'При отправке сообщения, текст автоматически отправится всем без возможности отмены!',
                                  reply_markup=delete_message_keyboard())
    await state.update_data(mess_del=mess_del,)
    await state.set_state(NewMessageForAll.waiting_message)


@router.message(NewMessageForAll.waiting_message)
async def all_send_message_state(message: types.Message, state: FSMContext):
    telegram_ids = await users_repo.get_all_users()
    for telegram_id in telegram_ids:
        await message.bot.send_message(chat_id=telegram_id,
                                       text=message.text)
    await state.clear()


@router.callback_query(F.data.startswith("delete_message:"))
@authorization(["creator", "administrator", "users"])
async def delete_message(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.delete()