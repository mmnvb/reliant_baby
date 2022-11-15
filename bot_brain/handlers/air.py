from aiogram import Bot, Dispatcher
from aiogram.types import Message
from asyncio import gather

import requests
from bs4 import BeautifulSoup

from bot_brain.data_base.users_db import get_all_user


async def send_message_cron(bot: Bot):
    await (users := gather(get_all_user()))
    users = users.result()[0]
    await (daily_text := gather(get_whether_msg()))
    for user in users:
        await bot.send_message(user[0], daily_text.result()[0])


async def give_air(msg: Message):
    await (daily_text := gather(get_whether_msg()))
    await msg.answer(daily_text.result()[0])


async def get_whether_msg():
    req = requests.get('https://www.iqair.com/uzbekistan/toshkent-shahri/tashkent')
    src = req.text

    # with open("index.html", 'w', encoding="utf-8") as file:
    #     file.write(req.text)
    #
    # with open("index.html", 'r', encoding="utf-8") as file:
    #     src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    text = soup.find('tr', class_='today').text.split()
    air_index = int(text[len(text)-5])

    # temperature = text[3].removeprefix('AQI').replace('°', '°-').removesuffix('-')
    temperature = text[len(text)-3].removeprefix('AQI').split('°')
    temperature = sorted(temperature, reverse=True)

    air_comment = "-"
    air_smile = "-"
    if air_index < 51:
        air_comment = 'чистый'
        air_smile = '🟢'
    elif 101 > air_index > 50:
        air_comment = 'средний'
        air_smile = '🟡'
    elif 151 > air_index > 100:
        air_comment = 'нездоровый для чувст. групп'
        air_smile = '🟠'
    elif 201 > air_index > 150:
        air_comment = 'нездоровый'
        air_smile = '🟠'
    elif 301 > air_index > 200:
        air_comment = 'опасный'
        air_smile = '🔴'
    elif air_index > 300:
        air_comment = 'Очень опасный'
        air_smile = '⚫'

    respond_text = f"🌦Сегодня в Ташкенте {temperature[0]}° - {temperature[1]}° " \
                   f"{'холода' if temperature[1].startswith('-') else 'тепла'}\n\n" \
                   f"{air_smile}Воздух: <b>{air_index}</b> (AQI)\n<i>( {air_comment} )</i>\n\n" \
                   f"Берегите себя, хорошего дня шеф❤"
    return respond_text


def register_air_requests(dp: Dispatcher):
    dp.register_message_handler(give_air, commands='air')
