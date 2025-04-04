import asyncio

import aiogram.exceptions
from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.keyboards.base_keyboards import back_base_menu
from bot.keyboards.headlines_keyboard import sources_menu_auto, sources_menu
from bot.middleware.authorization import authorization
from database.repositories.bot_config_repo import bot_config
from database.repositories.news_sources_repo import news_sources_repository
from database.repositories.source_subscriptions_repo import sources_subscriptions

router = Router(name="Базовая клавиатура")


@router.callback_query(F.data == 'get_sources_hand')
@authorization(["creator", "administrator", "users"])
async def get_sources_hand(callback_query: types.CallbackQuery,
                             state: FSMContext,
                             ) -> None:

    await callback_query.message.edit_text(text=f"Выберите источник новостей:",
                                               reply_markup=await sources_menu())


@router.callback_query(F.data == 'get_sources_auto')
@authorization(["creator", "administrator", "users"])
async def get_sources_auto(callback_query: types.CallbackQuery,
                             state: FSMContext,
                             ) -> None:

    await callback_query.message.edit_text(text=f"Выберите источники, с которых желаете получать новости.",
                                           reply_markup=await sources_menu_auto(callback_query.from_user.id))


@router.callback_query(F.data == 'about_text')
@authorization(["creator", "administrator", "users"])
async def about_text(callback_query: types.CallbackQuery,
                             state: FSMContext,
                             ) -> None:

    await callback_query.message.edit_text(text=await bot_config.get_about_text(),
                                           reply_markup=back_base_menu())


@router.callback_query(F.data == 'faq_text')
@authorization(["creator", "administrator", "users"])
async def faq_text(callback_query: types.CallbackQuery,
                             state: FSMContext,
                             ) -> None:
    await callback_query.message.edit_text(text=await bot_config.get_faq_text(),
                                           reply_markup=back_base_menu())


