from asyncio import gather
from sqlite3 import IntegrityError

from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import BotKicked, BotBlocked, ChatNotFound, ChatIdIsEmpty

from bot_brain.data_base.users_db import register_user_db, delete_user, get_user_config, update_music_db, \
    update_motive_db, update_weather_db, get_all_user
from bot_brain.keyboards.inlne_admin import main_menu, remove_keyboard, user_callback, edit_keyboard, property_kb, \
    choice_callback, post_callback, post_kb
from bot_brain.misc.states import FsmAdmin, FsmPost


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


# =========== MISC ================
async def backup(msg: Message):
    await msg.answer_document(open('users.db', 'rb'))


async def admin_main(call: CallbackQuery):
    await call.message.edit_text('⚙️Admin panel')
    await call.message.edit_reply_markup(main_menu)


async def finish_all(msg: Message, state: FSMContext):
    await state.finish()
    await msg.answer("Отменил")


# =========== EDIT ================
async def start_edit(call: CallbackQuery):
    await edit_keyboard(call)


async def change_properties(call: CallbackQuery, callback_data: dict):
    await (data := gather(get_user_config(callback_data.get('id'))))
    await call.message.edit_reply_markup(property_kb(callback_data.get('id'), data.result()[0]))


async def change_music(call: CallbackQuery, callback_data: dict):
    index = (1 if callback_data.get('i') == '0' else 0)
    await update_music_db(callback_data.get('id'), index)
    await call.answer(f"Has been changed to {index}", show_alert=True)
    await change_properties(call, callback_data)


async def change_motive(call: CallbackQuery, callback_data: dict):
    index = (1 if callback_data.get('i') == '0' else 0)
    await update_motive_db(callback_data.get('id'), index)
    await call.answer(f"Has been changed to {index}", show_alert=True)
    await change_properties(call, callback_data)


async def change_weather(call: CallbackQuery, callback_data: dict):
    index = (1 if callback_data.get('i') == '0' else 0)
    await update_weather_db(callback_data.get('id'), index)
    await call.answer(f"Has been changed to {index}", show_alert=True)
    await change_properties(call, callback_data)


# ===== POST =====
async def start_post(call: CallbackQuery):
    await call.message.delete()
    await FsmPost.content.set()
    await call.message.answer("💬Введите текст поста")


async def handle_post(msg: Message):
    await msg.answer(f"Ваш пост\n\n"
                     f"<i>{msg.text}</i>\n\n"
                     f"Отправить его?", reply_markup=post_kb(msg.text))


async def send_post(call: CallbackQuery, callback_data: dict):
    await call.answer("Начинаю...")
    await (users := gather(get_all_user()))
    users = users.result()[0]

    counter = 0
    for i in users:
        try:
            await call.bot.send_message(i[0], callback_data.get("text"))
        except (BotBlocked, BotKicked, ChatNotFound, ChatIdIsEmpty, Exception):
            counter += 1
    await call.message.delete()
    await call.message.answer(f"🟢Пост отправлен {len(users)-counter}/{len(users)}")


async def cancel_post(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await state.finish()
    await call.answer("Отменила")
    await call.message.delete()


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_panel, commands='admin', is_admin=True)
    dp.register_message_handler(backup, commands='backup', is_admin=True)
    # add
    dp.register_callback_query_handler(start_add, text='add')
    dp.register_message_handler(set_new_user, lambda msg: len(msg.text) > 6 and msg.text[1::].isnumeric(),
                                state=FsmAdmin.new_id)
    dp.register_message_handler(save_user, state=FsmAdmin.name, content_types='text')
    # remove
    dp.register_callback_query_handler(start_remove, text='remove')
    dp.register_callback_query_handler(user_option, user_callback.filter(method='select remove'))
    # back
    dp.register_callback_query_handler(admin_main, text='back_main')
    dp.register_message_handler(finish_all, state=FsmAdmin, commands='finish')
    # edit
    dp.register_callback_query_handler(start_edit, text=['edit', "back"])
    dp.register_callback_query_handler(change_properties, user_callback.filter(method='select edit'))
    dp.register_callback_query_handler(change_music, choice_callback.filter(method='edit_music'))
    dp.register_callback_query_handler(change_motive, choice_callback.filter(method='edit_motive'))
    dp.register_callback_query_handler(change_weather, choice_callback.filter(method='edit_weather'))
    # post
    dp.register_callback_query_handler(start_post, text="post", is_admin=True)
    dp.register_message_handler(handle_post, state=FsmPost.content)
    dp.register_callback_query_handler(cancel_post, post_callback.filter(method="no"), state=FsmPost.content)
    dp.register_callback_query_handler(send_post, post_callback.filter(method="yes"), state=FsmPost.content)

