from aiogram.dispatcher import Dispatcher
from aiogram.types import Message

from bot_brain.misc.convert_audio import ogg_to_mp3
from os import remove


async def ogg(msg: Message):
    await msg.bot.download_file_by_id(msg.voice.file_id, f"temp/{msg.from_user.id}.ogg")
    try:
        await ogg_to_mp3(msg.from_user.id, msg.forward_from.first_name)
    except AttributeError:
        await ogg_to_mp3(msg.from_user.id, msg.forward_sender_name)
    finally:
        await msg.answer_audio(open(f'temp/{msg.from_user.id}.mp3', "rb"))
        remove(f"temp/{msg.from_user.id}.mp3")


def register_covert(dp: Dispatcher):
    dp.register_message_handler(ogg, content_types='voice', in_db=True)
