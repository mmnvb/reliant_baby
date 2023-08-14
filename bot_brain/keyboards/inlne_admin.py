from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot_brain.data_base.users_db import get_all_user
from asyncio import gather
from aiogram.types import CallbackQuery
from aiogram.utils.callback_data import CallbackData

user_callback = CallbackData("self", "method", "id", 'name')
choice_callback = CallbackData("self", "method", "id", 'i')
post_callback = CallbackData("self", "method", "text")

main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('📝Edit', callback_data='edit')],
    [InlineKeyboardButton('➕Add', callback_data='add'),
     InlineKeyboardButton('🗑Remove', callback_data='remove')],
    [InlineKeyboardButton("✍️Post", callback_data="post")]
])


async def remove_keyboard(call: CallbackQuery):
    await (users := gather(get_all_user()))
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('🔙Back', callback_data='back_main')]
    ])
    for i in users.result()[0]:
        keyboard.add(InlineKeyboardButton("👤"+i[1],
                                          callback_data=user_callback.new(method='select remove',
                                                                          name=i[1],
                                                                          id=i[0])))
    await call.message.edit_text('🕵️‍♀️Here is the list of them')
    await call.message.edit_reply_markup(keyboard)


async def edit_keyboard(call: CallbackQuery):
    await (users := gather(get_all_user()))
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('🔙Back', callback_data='back_main')]
    ])
    for i in users.result()[0]:
        keyboard.add(InlineKeyboardButton("👤"+i[1],
                                          callback_data=user_callback.new(method='select edit',
                                                                          name=i[1],
                                                                          id=i[0])))
    await call.message.edit_text('🕵️‍♀️Here is the list of them')
    await call.message.edit_reply_markup(keyboard)


def property_kb(user_id, choices: tuple):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(f"🎵Тональность: {'✅' if choices[0]==1 else '🔴'}",
                              callback_data=choice_callback.new(method='edit_music', id=user_id, i=choices[0]))],
        [InlineKeyboardButton(f"⚡️Мотивация: {'✅' if choices[1] == 1 else '🔴'}",
                              callback_data=choice_callback.new(method='edit_motive', id=user_id, i=choices[1]))],
        [InlineKeyboardButton(f"⛅️Погода: {'✅' if choices[2] == 1 else '🔴'}",
                              callback_data=choice_callback.new(method='edit_weather', id=user_id, i=choices[2]))],
        [InlineKeyboardButton(f"🔙Назад", callback_data='back')]
    ])


def property_kb_user(user_id, choices: tuple):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(f"🎵Тональность: {'✅' if choices[0]==1 else '🔴'}",
                              callback_data=choice_callback.new(method='edit_music', id=user_id, i=choices[0]))],
        [InlineKeyboardButton(f"⚡️Мотивация: {'✅' if choices[1] == 1 else '🔴'}",
                              callback_data=choice_callback.new(method='edit_motive', id=user_id, i=choices[1]))],
        [InlineKeyboardButton(f"⛅️Погода: {'✅' if choices[2] == 1 else '🔴'}",
                              callback_data=choice_callback.new(method='edit_weather', id=user_id, i=choices[2]))],
        [InlineKeyboardButton(f"🔙Назад", callback_data='back')]
    ])


def post_kb(content):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("✅Да", callback_data=post_callback.new(method="yes",
                                                                     text=f"{content}"))],
        [InlineKeyboardButton("❌Нет", callback_data=post_callback.new(method="no",
                                                                      text='-'))]
    ])
