import asyncio

import aiogram.exceptions
from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.middleware.authorization import authorization

# from bot.middleware.authorization import authorization

router = Router(name="Базовая клавиатура")


@router.callback_query(F.data == 'buy_ozon_bank')
# @authorization(["creator", "administrator", "users"])
async def buy_ozon_bank(callback_query: types.CallbackQuery):

    try:
        await callback_query.message.edit_text(text=f"Описание товара",
                                               reply_markup=ozon_keyboard())
    except aiogram.exceptions.TelegramBadRequest:
        await callback_query.answer()


@router.callback_query(F.data == 'about_text')
@authorization(["creator", "administrator", "users"])
async def buy_gk(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(text='O nas',
                                           reply_markup=back_base_menu())


@router.callback_query(F.data == 'faq_text')
@authorization(["creator", "administrator", "users"])
async def faq_text(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(text='faq ....',
                                           reply_markup=back_base_menu())


@router.callback_query(F.data == 'all_life_ref_link')
# @authorization(["creator", "administrator", "users"])
async def all_life_ref_link(callback_query: types.CallbackQuery):
    bot_name = await callback_query.bot.get_me()
    await callback_query.message.edit_text(text=f'Ваша реферальная ссылка:\n\n'
                                                f'https://t.me/{bot_name.username}?start={callback_query.from_user.id}',
                                           reply_markup=back_ref_menu())

