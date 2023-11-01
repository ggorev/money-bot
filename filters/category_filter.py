from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from keyboards.default import *


class IsCategory(BoundFilter):
    async def check(self, message: Message) -> bool:
        return message.text in [shopping, family, gifts, health, transport, products, cafe, leisure]
