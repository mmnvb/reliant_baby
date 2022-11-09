from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot_brain.data_base.users_db import get_all_user
from asyncio import gather
from aiogram.types import CallbackQuery
from aiogram.utils.callback_data import CallbackData

user_callback = CallbackData("self", "method", "id", 'name')

main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('➕Add', callback_data='add')],
    [InlineKeyboardButton('🗑Remove', callback_data='remove')]
])


async def remove_keyboard(call: CallbackQuery):
    await (users := gather(get_all_user()))
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('👁Hide', callback_data='hide')]
    ])
    for i in users.result()[0]:
        keyboard.add(InlineKeyboardButton("👤"+i[1],
                                          callback_data=user_callback.new(method='select remove',
                                                                          name=i[1],
                                                                          id=i[0])))
    await call.message.edit_text('🕵️‍♀️Here is the list of them')
    await call.message.edit_reply_markup(keyboard)

