import asyncio

import aiogram.exceptions
from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.keyboards.base_keyboards import back_base_menu, sources_menu
from bot.middleware.authorization import authorization
from database.repositories.news_sources_repo import news_sources_repository

router = Router(name="Базовая клавиатура")


@router.callback_query(F.data == 'get_sources_hand')
@authorization(["creator", "administrator", "users"])
async def get_sources_hand(callback_query: types.CallbackQuery,
                             state: FSMContext,
                             ) -> None:
    sources = await news_sources_repository.get_all_source()
    await callback_query.message.edit_text(text=f"Выберите источник новостей:",
                                               reply_markup=sources_menu(sources))


@router.callback_query(F.data == 'get_sources_auto')
@authorization(["creator", "administrator", "users"])
async def get_sources_auto(callback_query: types.CallbackQuery,
                             state: FSMContext,
                             ) -> None:
    await callback_query.message.edit_text(text=f"Выберите источники, с которых желаете получать новости.",
                                           reply_markup=back_base_menu())


@router.callback_query(F.data == 'about_text')
@authorization(["creator", "administrator", "users"])
async def about_text(callback_query: types.CallbackQuery,
                             state: FSMContext,
                             ) -> None:

    await callback_query.message.edit_text(text='O nas',
                                           reply_markup=back_base_menu())


@router.callback_query(F.data == 'faq_text')
@authorization(["creator", "administrator", "users"])
async def faq_text(callback_query: types.CallbackQuery,
                             state: FSMContext,
                             ) -> None:
    await callback_query.message.edit_text(text='faq ....',
                                           reply_markup=back_base_menu())


@router.callback_query(F.data == 'all_life_ref_link')
@authorization(["creator", "administrator", "users"])
async def all_life_ref_link(callback_query: types.CallbackQuery,
                             state: FSMContext,
                             ) -> None:
    bot_name = await callback_query.bot.get_me()
    await callback_query.message.edit_text(text=f'Ваша реферальная ссылка:\n\n'
                                                f'https://t.me/{bot_name.username}?start={callback_query.from_user.id}',
                                           reply_markup=back_base_menu())

