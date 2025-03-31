from datetime import datetime

from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Union

from bot.keyboards.admin_keyboards import start_admin_panel
from bot.keyboards.base_keyboards import get_start_keyboard, start_base_panel
from bot.middleware.authorization import authorization
from database.repositories.users_repo import UserRepository
from database.session import db

# from bot.middleware.authorization import authorization


router = Router(name="Старт бота")


# Главное меню создателя
@router.message(CommandStart())
@authorization(["creator", "administrator", "users"])
async def command_start_menu_handler(message: types.Message, state: FSMContext):
    await state.clear()
    telegram_id = message.from_user.id
    async with db.session():
        user_repo = UserRepository(db)
        await user_repo.create_user(telegram_id=telegram_id,
                                    username=message.from_user.username,)


    await message.bot.send_message(chat_id=telegram_id,
                                   text=f"Привет. Ты попал на новостной бот headlines.\n\n"
                                        f"Ознакомиться с работой бота можно в - FAQ\n\n"
                                        f"Данный бот предназначен для получения новостей в самостоятельно или автоматическом режиме.\n",
                                   reply_markup=get_start_keyboard())


@router.message(F.text == "📝 Главное меню")
@router.callback_query(F.data == 'back_start_menu')
@authorization(["creator", "administrator", "users"])
async def start_menu_handler(event: Union[types.Message, CallbackQuery], state: FSMContext):
    await state.clear()

    try:
        await event.message.edit_text(
            text=f"Привет. Ты попал на новостной бот headlines.\n\n"
                                        f"Ознакомиться с работой бота можно в - FAQ\n\n"
                                        f"Данный бот предназначен для получения новостей в самостоятельно или автоматическом режиме.\n",
            reply_markup=get_start_keyboard())
    except:
        await event.answer(
            text=f"Привет. Ты попал на новостной бот headlines.\n\n"
                                        f"Ознакомиться с работой бота можно в - FAQ\n\n"
                                        f"Данный бот предназначен для получения новостей в самостоятельно или автоматическом режиме.\n",
            reply_markup=get_start_keyboard())
