from aiogram.dispatcher.filters.state import State, StatesGroup


class ExpenseState(StatesGroup):
    category = State()
    expense = State()
