from aiogram.dispatcher.filters.state import StatesGroup, State


class FsmAdmin(StatesGroup):
    new_id = State()
    name = State()


class FsmPost(StatesGroup):
    content = State()
