from aiogram.dispatcher import Dispatcher
from aiogram.types import Message

from bot_brain.misc.convert_audio import ogg_to_mp3, m4a_to_mp3
from os import remove


async def ogg(msg: Message):
    await msg.bot.download_file_by_id(msg.voice.file_id, f"temp/{msg.from_user.id}.ogg")
    try:
        await ogg_to_mp3(msg.from_user.id, msg.forward_from.first_name)
    except AttributeError:
        await ogg_to_mp3(msg.from_user.id, msg.forward_sender_name)
    finally:
        await msg.bot.send_chat_action(msg.chat.id, 'upload_audio')
        await msg.answer_audio(open(f'temp/{msg.from_user.id}.mp3', "rb"))
        remove(f"temp/{msg.from_user.id}.mp3")


async def m4a(msg: Message):
    if msg.audio.mime_type == 'audio/mp4':
        temp = await msg.answer("💾Скачивание началось")
        await msg.bot.download_file_by_id(msg.audio.file_id, f"temp/{msg.from_user.id}.m4a")
        await temp.edit_text('🔄Конвертация')
        await m4a_to_mp3(msg.from_user.id, msg.audio.performer, msg.audio.title)
        await temp.delete()
        await msg.bot.send_chat_action(msg.chat.id, 'upload_audio')
        await msg.answer_audio(open(f'temp/{msg.from_user.id}.mp3', 'rb'), thumb=msg.audio.thumb.file_id)
        remove(f'temp/{msg.from_user.id}.mp3')


def register_covert(dp: Dispatcher):
    dp.register_message_handler(ogg, content_types='voice', in_db=True)
    dp.register_message_handler(m4a, content_types='audio', in_db=True)
