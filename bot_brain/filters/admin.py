import typing

from aiogram.dispatcher.filters import BoundFilter
from config import ADMIN


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin: typing.Optional[bool] = None):
        self.is_admin = is_admin

    async def check(self, obj):
        if self.is_admin is None:
            return False
        return (str(obj.from_user.id) == ADMIN) == self.is_admin
