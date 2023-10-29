from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message

from filters import IsCategory
from keyboards.default import *
from loader import dp
from states import ExpenseState


@dp.message_handler(CommandStart())
async def bot_start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}! Чтобы добавить расход, выберите категорию из меню.",
                         reply_markup=category_markup())
    await ExpenseState.category.set()


@dp.message_handler(state=ExpenseState.category)
@dp.message_handler(IsCategory())
async def set_category(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text
    await ExpenseState.expense.set()
    await message.answer('Отлично! Теперь введите сумму расхода.', reply_markup=cancel_expense_markup())


@dp.message_handler(text=cancel_expense_message, state=ExpenseState.expense)
@dp.message_handler(text=cancel_expense_message, state=ExpenseState.notes)
async def process_cancel(message: Message, state: FSMContext):
    await message.answer('Ок, отменено!', reply_markup=category_markup())
    await state.finish()


@dp.message_handler(state=ExpenseState.expense)
async def set_expense(message: Message, state: FSMContext):
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add('Нет')
    async with state.proxy() as data:
        data['expense'] = message.text
    await ExpenseState.next()
    await message.answer('Хорошо, есть ли у Вас комментарий к расходу? Если нет, просто отправьте "Нет".',
                         reply_markup=before_add_amount_markup())


@dp.message_handler(text=edit_amount_message, state=ExpenseState.notes)
async def process_cancel(message: Message, state: FSMContext):
    await ExpenseState.expense.set()
    await message.answer('Введите сумму расхода.', reply_markup=cancel_expense_markup())


@dp.message_handler(state=ExpenseState.notes)
async def set_category(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['notes'] = message.text
        if data['notes'] == 'Нет':
            await message.answer(
                f"Расход : {data['expense']} RUB\nКатегория: {data['category']}\n", reply_markup=category_markup())
        else:
            await message.answer(
                f"Расход : {data['expense']} RUB\nКатегория: {data['category']}\nКомментарий: {data['notes']}",
                reply_markup=category_markup())
    await state.finish()
