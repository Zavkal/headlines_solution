import asyncio

import aiogram.exceptions
from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.keyboards.base_keyboards import back_base_menu, sources_menu
from bot.middleware.authorization import authorization
from database.repositories.headlines_repo import headlines_repo
from database.repositories.news_sources_repo import news_sources_repository


router = Router(name="Выдача заголовков")


class NewCounterHeadlines(StatesGroup):
    waiting_message = State()


@router.callback_query(F.data.startswith('get_headlines_hand:'))
@authorization(["creator", "administrator", "users"])
async def get_headlines_hand(callback_query: types.CallbackQuery,
                             state: FSMContext,
                             ) -> None:
    data = callback_query.data.split(":")
    source_id = int(data[1])

    msg_callback = await callback_query.message.answer(text=f"Укажите сколько важных новостей хотите получить:")
    await state.update_data(msg_callback=msg_callback, source_id=source_id)
    await state.set_state(NewCounterHeadlines.waiting_message)


@router.message(NewCounterHeadlines.waiting_message)
async def get_headlines_hand_state(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    msg_callback = user_data.get('msg_callback')
    source_id = user_data.get('source_id')
    try:
        counter = int(message.text)
        news = await headlines_repo.get_news(source_id=source_id, counter=counter)


    except Exception:
        msg_del = await message.answer('Введите число. Другие данные бот не принимает.')
        await asyncio.sleep(2)
        await msg_del.delete()

    await message.delete()





