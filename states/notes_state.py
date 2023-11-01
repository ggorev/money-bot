from aiogram.dispatcher.filters.state import State, StatesGroup


class NotesState(StatesGroup):
    notes = State()