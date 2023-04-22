from aiogram.dispatcher import Dispatcher
from aiogram.types import Message
from pytube import Search
from os import remove
from random import choice, shuffle


async def test_func(msg: Message):
    try:
        motive = ["Andrew Tate motivation #shorts", "No Fap motivation #shorts", "Reject modernity #shorts",
                  "callisthenics insane motivation #shorts", "embrace greatness #shorts", "exposed the matrix #shorts",
                  "воркаут мотивация #shorts", "игорь войтенко мотивация #shorts"]
        print('search started')
        print(x := choice(motive) + " was selected")
        s = Search(x)
        shuffle(s.results)
        for i in s.results:
            i.streams.filter(file_extension='mp4')
            video = i.streams.get_by_itag(22)
            if round(video.filesize_approx / 1000000) <= 10:
                print('downloading')
                video.download(filename='11.mp4')
                print('uploading..')
                await msg.answer_video(open('11.mp4', 'rb'))
                remove("11.mp4")
                break
    except KeyError:
        await msg.answer('went wrong')
        await test_func(msg)


def register_motivation(dp: Dispatcher):
    dp.register_message_handler(test_func, commands='test')
