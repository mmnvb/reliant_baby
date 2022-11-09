from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

yt_call = CallbackData("self", "resolution", 'yt_object')


def yt_options(data):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='💾360p',
                              callback_data=yt_call.new(
                                                        resolution='low',
                                                        yt_object=data))],
        [InlineKeyboardButton(text='💾720p',
                              callback_data=yt_call.new(
                                                        resolution='high',
                                                        yt_object=data))],
        [InlineKeyboardButton(text='🎧Audio',
                              callback_data=yt_call.new(
                                                        resolution='audio',
                                                        yt_object=data))]
    ])
