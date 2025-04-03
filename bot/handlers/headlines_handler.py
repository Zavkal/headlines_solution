import asyncio

from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.keyboards.headlines_keyboard import sources_menu_auto
from bot.middleware.authorization import authorization
from bot.operations.generate_text_headlines import generate_text
from database.repositories.headlines_repo import headlines_repo
from database.repositories.source_subscriptions_repo import sources_subscriptions

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
    source_name = data[2]

    msg_callback = await callback_query.message.answer(text=f"Укажите сколько важных новостей хотите получить:")
    await callback_query.answer()
    await state.update_data(msg_callback=msg_callback, source_id=source_id, source_name=source_name)
    await state.set_state(NewCounterHeadlines.waiting_message)


@router.message(NewCounterHeadlines.waiting_message)
async def get_headlines_hand_state(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    msg_callback = user_data.get('msg_callback')
    source_id = user_data.get('source_id')
    source_name = user_data.get('source_name')
    await message.delete()
    try:
        counter = int(message.text)
        if  1 < counter < 21:
            headlines = await headlines_repo.get_news(source_id=source_id, counter=counter)
            for headline in headlines:
                text = await generate_text(headline=headline, source_name=source_name)
                await message.answer(text=text,
                                     parse_mode='HTML',
                                     disable_web_page_preview=True)
            await msg_callback.delete()

        else:
            msg_del = await message.answer(text='Введите число не более 20 и не менее 1')
            await asyncio.sleep(2)
            await msg_del.delete()

    except Exception:
        msg_del = await message.answer('Введите число. Другие данные бот не принимает.')
        await asyncio.sleep(2)
        await msg_del.delete()
    await state.clear()


@router.callback_query(F.data.startswith('del_or_add_subscription:'))
@authorization(["creator", "administrator", "users"])
async def del_or_add_subscription(callback_query: types.CallbackQuery,
                             state: FSMContext,
                             ) -> None:
    data = callback_query.data.split(":")
    source_id = int(data[1])
    is_subscription = data[2]
    telegram_id = callback_query.from_user.id
    if is_subscription == 'True':
        await sources_subscriptions.delete_subscription(telegram_id=telegram_id,
                                                        source_id=source_id)
    else:
        await sources_subscriptions.create_subscription(telegram_id=telegram_id,
                                                     source_id=source_id)

    await callback_query.message.edit_text(text=f"Выберите источники с которых желаете получать новости.",
                                                       reply_markup=await sources_menu_auto(telegram_id=telegram_id))
    await callback_query.answer()





