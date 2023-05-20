from aiogram.dispatcher import Dispatcher
from aiogram.types import Message
from aiogram import Bot
from aiogram.utils.exceptions import BotBlocked, ChatNotFound, BotKicked

from pytube import Search
from pytube.exceptions import AgeRestrictedError

from os import remove
from random import choice, shuffle, randint
import logging

logger = logging.getLogger(__name__)


async def send_motivation(bot: Bot, user_ids: list, call_from: int = 1):
    logger.info('Started search for motivation')
    try_count = 0
    max_attempts = 7

    while try_count < max_attempts:
        try:
            # get random topic
            motive = ["Andrew Tate motivation #shorts", "No Fap motivation #shorts", "Reject modernity #shorts",
                      "callisthenics insane motivation #shorts", "embrace greatness #shorts",
                      "exposed the matrix #shorts", "inspirational quotes #shorts"
                      "воркаут мотивация #shorts", "игорь войтенко мотивация #shorts"]

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
                            pass
                    # clear and stop
                    remove(f'temp/{call_from}.mp4')
                    break
            break
        except (KeyError, AgeRestrictedError, Exception):
            try_count += 1
    else:
        logger.error('Cannot parse Youtube motivation after multiple attempts')


async def test_func(msg: Message):
    await send_motivation(msg.bot, [msg.chat.id], msg.from_user.id)


def register_motivation(dp: Dispatcher):
    dp.register_message_handler(test_func, commands='test')
