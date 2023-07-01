from aiogram.dispatcher import Dispatcher
from aiogram.types import Message
from aiogram import Bot
from aiogram.utils.exceptions import BotBlocked, ChatNotFound, BotKicked

from pytube import Search
from pytube.exceptions import AgeRestrictedError

from bot_brain.data_base.users_db import get_motive_user

from os import remove
from random import choice, shuffle, randint
from logging import getLogger
from asyncio import gather
from config import motive

logger = getLogger(__name__)


async def send_daily_motivation(bot: Bot):
    await (users := gather(get_motive_user()))
    users = users.result()[0]
    await send_motivation(bot, [i[0] for i in users])


async def send_motivation(bot: Bot, user_ids: list, call_from: int = 1):
    logger.info('Started search for motivation')
    try_count = 0
    max_attempts = 7

    while try_count < max_attempts:
        try:
            # get random topic
            s = Search(choice(motive))
            shuffle(s.results)
            # look for proper one
            for i in s.results:
                i.streams.filter(file_extension='mp4')
                video = i.streams.get_by_itag(22)
                if round(video.filesize_approx / 1000000) <= randint(1, 9):
                    # download proper video
                    video.download(filename=f'temp/{call_from}.mp4')
                    # start sending
                    for r in user_ids:
                        try:
                            await bot.send_video(r, open(f'temp/{call_from}.mp4', 'rb'))
                        except (BotBlocked, BotKicked, ChatNotFound):
                            logger.warning(f'Cannot send motivation to {r}')
                    # clear and stop
                    remove(f'temp/{call_from}.mp4')
                    break
            break
        except (KeyError, AgeRestrictedError, Exception):
            try_count += 1
    else:
        logger.error('Cannot parse Youtube motivation after multiple attempts')


async def call_motivation(msg: Message):
    await msg.bot.send_chat_action(msg.chat.id, 'upload_video')
    await send_motivation(msg.bot, [msg.chat.id], msg.from_user.id)


def register_motivation(dp: Dispatcher):
    dp.register_message_handler(call_motivation, commands=['motivation', 'help'], in_db=True)
    dp.register_message_handler(call_motivation, text=["помоги", 'помощь', "мотивация", "вдохнови", "смотивируй",
                                                       "мне плохо"], in_db=True)
