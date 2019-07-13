from app import dp
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery, ContentTypes
from aiogram.utils.callback_data import CallbackData

like = CallbackData("like", "action")


@dp.channel_post_handler(content_types=ContentTypes.ANY)
async def new_post(m: Message):
    keyb = InlineKeyboardMarkup(row_width=2)
    keyb.add(InlineKeyboardButton(text="👍 0", callback_data=like.new(action=1)))
    keyb.add(InlineKeyboardButton(text="👎 0", callback_data=like.new(action=0)))
    await m.edit_reply_markup(keyb)
    await dp.current_state(chat=m.chat.id, user=m.chat.id).update_data(
        **{str(m.message_id): {"pos": 0, "neg": 0}})


@dp.callback_query_handler()
async def call(c: CallbackQuery, state: FSMContext):
    message_id = str(c.message.message_id)
    liked = int(c.data)
    await c.answer(f"Вам {'Понравилось' if liked else 'Не понравилось'}")

    ratings = (await dp.current_state(chat=c.message.chat.id,
                                      user=c.message.chat.id).get_data())
    ratings = ratings.get(message_id)
    pos = int(ratings.get("pos"))
    neg = int(ratings.get("neg"))

    async with state.proxy() as data:
        prev_like = data.get(message_id, None)
        data[message_id] = liked
        if prev_like is not None:
            if liked and prev_like:
                return
            elif not liked and not prev_like:
                return
            elif liked:
                pos += 1
                neg -= 1
            else:
                pos -= 1
                neg += 1
        else:
            if liked:
                pos += 1
            else:
                neg += 1

    keyb = InlineKeyboardMarkup(row_width=2)
    keyb.add(InlineKeyboardButton(text=f"👍 {pos}", callback_data=like.new(action=1)))
    keyb.add(InlineKeyboardButton(text=f"👎 {neg}", callback_data=like.new(action=0)))

    await c.message.edit_reply_markup(keyb)
    await dp.current_state(chat=c.message.chat.id,
                           user=c.message.chat.id).update_data(**{str(message_id): {"pos": pos, "neg": neg}})
