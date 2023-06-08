import logging
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

from aiogram import Dispatcher, Bot
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot_brain.handlers.air import send_message_cron
from bot_brain.handlers.youtube import register_youtube
from bot_brain.handlers.admin import register_admin_handlers
from bot_brain.handlers.air import register_air_requests
from bot_brain.handlers.motivation import register_motivation
from bot_brain.handlers.convert import register_covert
from bot_brain.middleware.antiflood import ThrottlingMiddleware
from bot_brain.data_base.users_db import db_start
from bot_brain.filters.user_in_db import UserInDB
from bot_brain.filters.admin import AdminFilter

logger = logging.getLogger(__name__)


def register_all_filters(dispatcher):
    dispatcher.filters_factory.bind(UserInDB)
    dispatcher.filters_factory.bind(AdminFilter)


def register_all_handlers(dispatcher):
    register_admin_handlers(dispatcher)
    register_motivation(dispatcher)
    register_air_requests(dispatcher)
    register_youtube(dispatcher)
    register_covert(dispatcher)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")

    storage = MemoryStorage()
    bot = Bot(TOKEN, parse_mode="HTML")
    dp = Dispatcher(bot, storage=storage)

    await db_start()

    scheduler = AsyncIOScheduler(timezone='Asia/Tashkent')
    scheduler.add_job(send_message_cron, trigger='cron', hour=7, minute=58, start_date=datetime.now(),
                      kwargs={'bot': bot})
    scheduler.start()

    dp.middleware.setup(ThrottlingMiddleware())
    register_all_filters(dp)
    register_all_handlers(dp)
    # start
    try:
        await dp.skip_updates()
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
