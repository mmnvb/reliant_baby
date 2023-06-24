from aiogram.dispatcher import Dispatcher
from aiogram.types import Message, ChatActions
from aiogram.utils.exceptions import FileIsTooBig

import instaloader
from instaloader.exceptions import InvalidArgumentException, PrivateProfileNotFollowedException

from os import path, remove


async def download_post_media(url, id_code: int):
    try:
        # set up
        loader = instaloader.Instaloader()
        post = instaloader.Post.from_shortcode(loader.context, url)

        # config
        loader.download_videos = post.is_video
        loader.download_pictures = not post.is_video
        if post.mediacount > 1:
            loader.download_videos, loader.download_pictures = True, True

        loader.download_geotags = False
        loader.download_video_thumbnails = False
        loader.download_comments = False
        loader.save_metadata = False
        loader.post_metadata_txt_pattern = ''
        # loader.context = False

        # download
        loader.filename_pattern = f"{id_code}"
        loader.dirname_pattern = f"temp/instagram"
        loader.download_post(post, target='')
        loader.close()
        return True, post.mediacount, post.is_video

    except (InvalidArgumentException, PrivateProfileNotFollowedException, Exception):
        return False, 0, 0


async def download_insta(msg: Message):
    try:
        # download
        status = await download_post_media(msg.text.split('/')[4], msg.from_user.id)
        assert status[0] is True

        # upload - MEDIA GROUP
        if status[1] > 1:
            await ChatActions.upload_photo()
            files = [f"{(x:= f'{msg.from_user.id}_{i}')}.{'mp4' if path.exists(f'temp/instagram/{x}.mp4') else 'jpg'}"
                     for i in range(1, status[1]+1)]
            response = await msg.answer_media_group([{"media": open(f"temp/instagram/{i}", 'rb'),
                                                    "type": f"{'photo' if i.endswith('.jpg') else 'video'}"}
                                                     for i in files])
            await response[0].edit_caption('Выполнил шеф❤')
            for file in files:
                remove(f"temp/instagram/{file}")
            return

        # VIDEO
        if status[2]:
            try:
                await ChatActions.upload_video()
                await msg.answer_video(open(f"temp/instagram/{msg.from_user.id}.mp4", 'rb'))
            except FileIsTooBig:
                await msg.answer('Файл слишком большой (50+мб)')
            finally:
                remove(f"temp/instagram/{msg.from_user.id}.mp4")
                return

        # PHOTO
        try:
            await ChatActions.upload_photo()
            await msg.answer_photo(open(f"temp/instagram/{msg.from_user.id}.jpg", 'rb'))
        except FileIsTooBig:
            await msg.answer('Файл слишком большой (50+мб)')
        finally:
            remove(f"temp/instagram/{msg.from_user.id}.jpg")
            return
    except AssertionError:
        await msg.answer("<b>😕Не получилось скачать ваш пост</b>\n\n"
                         "<i>Возможные причины:\n"
                         "- Вы отправили сторис\n"
                         "- Вы отправили пост закрытого профиля\n"
                         "- Вы отправили слишком большой IGTV</i>\n\n"
                         "Если это не так, то свяжитесь с Бобом👨‍💻")


def register_instagram(dp: Dispatcher):
    dp.register_message_handler(download_insta,
                                lambda l: (x := l.text).startswith('https://instagram') or x.startswith('https://www'
                                                                                                        '.instagram'),
                                in_db=True)
