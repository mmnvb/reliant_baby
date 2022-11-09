from aiogram.dispatcher import Dispatcher
from aiogram.types import Message


async def hello(msg: Message):
    await msg.answer(msg.text)


def register_echo(dp: Dispatcher):
    dp.register_message_handler(hello, in_db=True)
