from app import dp
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery, ContentTypes
from aiogram.utils.callback_data import CallbackData
import re
like = CallbackData("like", "action")


@dp.channel_post_handler(content_types=ContentTypes.ANY)
async def new_post(m: Message):
    keyb = InlineKeyboardMarkup(row_width=2)
    keyb.insert(InlineKeyboardButton(text="👍 0", callback_data=like.new(action=1)))
    keyb.insert(InlineKeyboardButton(text="👎 0", callback_data=like.new(action=0)))
    await m.edit_reply_markup(keyb)


@dp.callback_query_handler(like.filter())
async def call(c: CallbackQuery, state: FSMContext, callback_data: dict):
    message_id = str(c.message.message_id)
    liked = int(callback_data.get("action"))
    await c.answer(f"Вам {'Понравилось' if liked else 'Не понравилось'}")

    markup = c.message.reply_markup.inline_keyboard[0]
    pos = int(re.findall(r".+(\d+)", markup[0]["text"])[0])
    neg = int(re.findall(r".+(\d+)", markup[1]["text"])[0])

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
    keyb.insert(InlineKeyboardButton(text=f"👍 {pos}", callback_data=like.new(action=1)))
    keyb.insert(InlineKeyboardButton(text=f"👎 {neg}", callback_data=like.new(action=0)))
    await c.message.edit_reply_markup(keyb)
