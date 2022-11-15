from aiogram import Bot
from asyncio import gather


from bot_brain.data_base.users_db import get_all_user


async def send_message_cron(bot: Bot):
    await (users := gather(get_all_user()))
    users = users.result()[0]
    daily_text = '0'
    for user in users:
        await bot.send_message(user[0], daily_text)
