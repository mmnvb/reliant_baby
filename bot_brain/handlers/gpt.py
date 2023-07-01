import openai
from openai.error import RateLimitError, AuthenticationError, APIError, InvalidAPIType, ServiceUnavailableError, \
    APIConnectionError, InvalidRequestError, TryAgain, OpenAIError
from config import GPT_API

from aiogram.dispatcher import Dispatcher
from aiogram.types import Message, ChatActions
from aiogram.utils.exceptions import MessageTextIsEmpty

from logging import getLogger
logger = getLogger(__name__)

openai.api_key = GPT_API


async def evaluate(msg: Message):
    try:
        await ChatActions.typing()
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Ты играешь роль моего ассистента - Reliant Baby. Ты женского пола"},
                {"role": "user", "content": msg.text},
            ]
        )
        result = ''
        for choice in response.choices:
            result += choice.message.content
        try:
            await msg.answer(result)
        except MessageTextIsEmpty:
            ...
    except (RateLimitError, TryAgain):
        logger.warning("GPT rate limit has been reached or TRY again")
        await msg.answer('Я немного устала, не хочу отвечать🐥')
    except ServiceUnavailableError:
        logger.error('GPT services are unavailable')
        await msg.answer('Сейчас занята, пишите позже✌️')
    except InvalidRequestError:
        await msg.answer('Не отвечаю на такое')
    except (AuthenticationError, APIError, InvalidAPIType, APIConnectionError):
        logger.error("API CONNECTION ERROR IN GPT 3.5")
    except (OpenAIError, Exception):
        logger.error('Something went wrong')


async def start(msg: Message):
    await msg.answer(f'👋Это Reliant Baby, твой ID: <code>{msg.from_user.id}</code>')


def register_gpt(dp: Dispatcher):
    dp.register_message_handler(start, commands='start')
    dp.register_message_handler(evaluate, lambda x: len(x.text) < 200,
                                content_types='text', in_db=True)
