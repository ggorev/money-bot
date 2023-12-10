from aiogram.dispatcher.filters.state import State, StatesGroup


class StatisticsState(StatesGroup):
    select_day = State()
    date_from = State()
    date_to = State()
