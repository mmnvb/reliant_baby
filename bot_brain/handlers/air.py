from aiogram import Bot, Dispatcher
from aiogram.types import Message
from asyncio import gather
from aiogram.utils.exceptions import BotBlocked

import requests
from bs4 import BeautifulSoup

from bot_brain.data_base.users_db import get_all_user


async def send_message_cron(bot: Bot):
    await (users := gather(get_all_user()))
    users = users.result()[0]
    await (daily_text := gather(get_whether_msg()))
    for user in users:
        try:
            print(f"{user} tried")
            await bot.send_message(user[0], daily_text.result()[0])
        except [ConnectionResetError, BotBlocked, ConnectionError]:
            pass


async def give_air(msg: Message):
    await (daily_text := gather(get_whether_msg()))
    await msg.answer(daily_text.result()[0])


async def get_whether_msg():
    req = requests.get('https://www.iqair.com/uzbekistan/toshkent-shahri/tashkent')
    soup = BeautifulSoup(req.text, 'lxml')

    text = soup.find('tr', class_='today').text.split()
    air_index = int(text[len(text)-5])
    temperature = text[len(text)-3].removeprefix('AQI').split('°')
    temperature = sorted(temperature, reverse=True)

    if air_index < 51:
        air_comment, air_smile = 'чистый', '🟢'
    elif air_index < 101:
        air_comment, air_smile = 'средний', '🟡'
    elif air_index < 151:
        air_comment, air_smile = 'нездоровый для чувст. групп', '🟠'
    elif air_index < 201:
        air_comment, air_smile = 'нездоровый', '🟠'
    elif air_index < 301:
        air_comment, air_smile = 'опасный', '🔴'
    else:
        air_comment, air_smile = 'Очень опасный', '⚫'

    respond_text = f"🌦Сегодня в Ташкенте {temperature[0]}° - {temperature[1]}° " \
                   f"{'холода' if temperature[1].startswith('-') else 'тепла'}\n\n" \
                   f"{air_smile}Воздух: <b>{air_index}</b> (AQI)\n<i>( {air_comment} )</i>\n\n" \
                   f"Берегите себя, хорошего дня шеф❤"
    return respond_text


async def give_weather(msg: Message):
    req = requests.get('https://www.iqair.com/uzbekistan/toshkent-shahri/tashkent')
    soup = BeautifulSoup(req.text, 'lxml')

    data = [td.text for td in soup.find_all('td')]
    weather_icons = {
        "Clear sky": "☀️",
        "Few clouds": "🌤️",
        "Variable cloudiness": "⛅",
        "Broken clouds": "🌥️",
        "Scattered clouds": "🌤️",
        "Overcast": "☁️",
        "Mist": "🌁",
        "Fog": "🌁",
        "Rain": "🌧️",
        "Thunderstorm": "⛈️",
        "Snow": "❄️",
        "Blizzard": "🌨"
    }

    x = data.index('Today')
    tommorow = [data[x+6].split()[1], (data[x+8].split("°"))]

    await msg.answer(f"{weather_icons.get(data[1])}Сейчас в Ташкенте {data[3]}\n\n"
                     f"💧Влажность: {data[5]}\n"
                     f"🍃Ветер: {data[7]}\n\n"
                     f"<span class='tg-spoiler'>🗓Завтра {tommorow[1][1]}-{tommorow[1][0]}°C"
                     f" ({tommorow[0]} AQI)</span>")


def register_air_requests(dp: Dispatcher):
    dp.register_message_handler(give_air, commands='air')
    dp.register_message_handler(give_weather, commands='weather')
