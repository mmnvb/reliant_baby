from aiogram.dispatcher import Dispatcher
from aiogram.types import Message, CallbackQuery
from os import remove
from asyncio import gather

from pytube import YouTube
from pytube.exceptions import RegexMatchError, PytubeError, AgeRestrictedError

from bot_brain.keyboards.inline_user import yt_options, yt_call
from bot_brain.misc.coding import decode, encode
from bot_brain.misc.convert_audio import m4a_to_mp3
from bot_brain.misc.audio import find_key

from bot_brain.data_base.users_db import is_musician


async def evaluate_youtube(msg: Message):
    try:
        yt = YouTube(msg.text)
        caption_text = f"<b>{yt.title}</b>\n\n" \
                       f"👤<code>{yt.author}</code>"

        await msg.answer_photo(yt.thumbnail_url, caption=caption_text,
                               reply_markup=yt_options(encode(msg.text)))

    except RegexMatchError:
        await msg.answer('Нет видео по этой ссылке😕')

    except PytubeError:
        await msg.answer('Smth went wrong, try again')


async def download_high(call: CallbackQuery, callback_data: dict):
    await call.answer()
    await call.message.delete()
    try:
        yt = YouTube(decode(callback_data.get('yt_object')))
        yt.streams.filter(file_extension='mp4')
        video = yt.streams.get_highest_resolution()

        assert (size := round(video.filesize_approx / 1000000)) < 50

        await call.message.answer(f'💾Скачиваю шеф, файл весит {size} MB')
        video.download(filename=(file := f'temp/{call.from_user.id}.mp4'))
        await call.bot.delete_message(call.message.chat.id, call.message.message_id + 1)
        await call.bot.send_chat_action(call.message.chat.id, 'upload_video')
        await call.message.answer_video(open(file, 'rb'))
        remove(file)
    except AssertionError:
        await call.message.answer('🟡Я скачиваю максимум 50 мб, (это особенность Python разработки)')
    except KeyError:
        await call.message.answer('🔴Название ролика ломает мою систему :( не могу скачать')
    except AgeRestrictedError:
        await call.message.answer("🔞Видео имеет ограничение по возрасту. Пока что бот такое не скачивает")
    except (RegexMatchError, Exception):
        await call.message.answer("Что то пошло не так")


async def download_low(call: CallbackQuery, callback_data: dict):
    await call.answer()
    await call.message.delete()
    try:
        yt = YouTube(decode(callback_data.get('yt_object')))
        yt.streams.filter(file_extension='mp4')
        video = yt.streams.get_by_itag(18)

        assert (size := round(video.filesize_approx / 1000000)) < 50

        await call.message.answer(f'💾Скачиваю шеф, файл весит {size} MB')
        video.download(filename=(file := f'temp/{call.from_user.id}.mp4'))
        await call.bot.delete_message(call.message.chat.id, call.message.message_id+1)
        await call.bot.send_chat_action(call.message.chat.id, 'upload_video')
        await call.message.answer_video(open(file, 'rb'))
        remove(file)
    except AssertionError:
        await call.message.answer('🟡Я скачиваю максимум 50 мб (это особенность Python разработки)')
    except KeyError:
        await call.message.answer('🔴Название ролика ломает мою систему :( не могу скачать')
    except AgeRestrictedError:
        await call.message.answer("🔞Видео имеет ограничение по возрасту. Пока что бот такое не скачивает")
    except (RegexMatchError, Exception):
        await call.message.answer("Что то пошло не так")


async def download_audio(call: CallbackQuery, callback_data: dict):
    await call.answer()
    await call.message.delete()
    try:
        # evaluate
        yt = YouTube(decode(callback_data.get('yt_object')))
        yt.streams.filter(only_audio=True)
        video = yt.streams.get_by_itag(251)
        # download
        assert (size := round(video.filesize_approx / 1000000)) < 50
        await call.message.answer(f'💾Скачиваю шеф, файл весит {size} MB')
        video.download(filename=f'{call.from_user.id}.m4a',
                       output_path='temp')
        # convert and find
        await call.bot.edit_message_text('🔄 Конвертирую👨‍🔧', call.message.chat.id, call.message.message_id + 1)
        await m4a_to_mp3(call.from_user.id, yt.author, yt.title)

        # preference check (DB request)
        await (preference := gather(is_musician(call.from_user.id)))
        if preference.result()[0]:
            await call.bot.send_chat_action(call.message.chat.id, 'upload_audio')
            await call.message.answer_audio(open(f"temp/{call.from_user.id}.mp3", 'rb'))
            await call.bot.delete_message(call.message.chat.id, call.message.message_id + 1)
            remove(f"temp/{call.from_user.id}.mp3")
            return

        # if musician
        await call.bot.edit_message_text('🔎 Определяю тональность🎵', call.message.chat.id, call.message.message_id + 1)
        await (key := gather(find_key(call.from_user.id)))
        key = key.result()[0]
        try:
            # загрузка
            await call.bot.delete_message(call.message.chat.id, call.message.message_id + 1)
            await call.bot.send_chat_action(call.message.chat.id, 'upload_audio')
            await call.message.answer_audio(open(f"temp/{call.from_user.id}.mp3", 'rb'),
                                            caption=f"🎹Тональность: {key[0]}\n"
                                                    f"🎲Корреляция: {key[1]}\n\n"
                                                    f"🤷‍♂Альтернатива: {'-' if key[2]==0 else key[2]}, "
                                                    f"{'-' if key[3]==0 else key[3]}")
            remove(f"temp/{call.from_user.id}.mp3")
        except FileNotFoundError:
            await call.message.answer('Я не нашел файл который сам же скачал🙂')

    except AssertionError:
        await call.message.answer('🟡Я скачиваю максимум 50 мб аудио')
    except KeyError:
        await call.message.answer('🔴Название ролика ломает мою систему :(. Обратитесь админу для улучшения')
    except AgeRestrictedError:
        await call.message.answer("🔞Видео имеет ограничение по возрасту. Пока что бот такое не скачивает")
    except (RegexMatchError, Exception):
        await call.message.answer("Что то пошло не так")


def register_youtube(dp: Dispatcher):
    dp.register_message_handler(evaluate_youtube,
                                lambda l: (x := l.text).startswith('https://you') or x.startswith('https://www.you'),
                                in_db=True)
    dp.register_callback_query_handler(download_low, yt_call.filter(resolution='low'))
    dp.register_callback_query_handler(download_high, yt_call.filter(resolution='high'))
    dp.register_callback_query_handler(download_audio, yt_call.filter(resolution='audio'))
