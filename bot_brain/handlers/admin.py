from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import Message, CallbackQuery

from bot_brain.keyboards.inlne_admin import main_menu, remove_keyboard, user_callback
from bot_brain.misc.states import FsmAdmin
from bot_brain.data_base.users_db import register_user_db, delete_user
from sqlite3 import IntegrityError


async def admin_panel(msg: Message):
    await msg.answer('⚙<b>Admin panel</b>', reply_markup=main_menu)


# =========== ADD ================
async def start_add(call: CallbackQuery):
    await FsmAdmin.new_id.set()
    await call.answer()
    await call.message.delete()
    await call.message.answer('👨‍💻Отлично отправьте мне ID того кого хотите добавить')


async def set_new_user(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = msg.text
    await msg.answer('Найс, как их будем звать?👤')
    await FsmAdmin.name.set()


async def save_user(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = msg.text
    try:
        await register_user_db(user_id=data['id'], name=data['name'])
        await msg.answer('🟢Пользователь добавлен!')
    except IntegrityError:
        await msg.answer('🟡Он уже был в базе чел')
    await state.finish()


# =========== REMOVE ================
async def start_remove(call: CallbackQuery):
    await remove_keyboard(call)


async def user_option(call: CallbackQuery, callback_data: dict):
    await delete_user(callback_data.get('id'))
    await call.answer()
    await call.message.answer(f"🟢<i>{callback_data.get('name')}</i>"
                              f" with ID = <code>{callback_data.get('id')}</code> was removed🗑")
    await call.message.delete()


async def hide_menu(call: CallbackQuery):
    await call.message.delete()


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_panel, commands='admin', is_admin=True)
    # add
    dp.register_callback_query_handler(start_add, text='add')
    dp.register_message_handler(set_new_user, lambda msg: len(msg.text) > 6,
                                state=FsmAdmin.new_id)
    dp.register_message_handler(save_user, state=FsmAdmin.name, content_types='text')
    # remove
    dp.register_callback_query_handler(start_remove, text='remove')
    dp.register_callback_query_handler(user_option, user_callback.filter(method='select remove'))
    # back / hide
    dp.register_callback_query_handler(hide_menu, text='hide')
