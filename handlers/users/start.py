from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message, CallbackQuery

from filters import IsCategory
from keyboards.default import *
from keyboards.inline import *
from loader import dp, bot, db
from states import ExpenseState, NotesState
from utils.start import get_total_daily_expenses, get_expense_values


@dp.message_handler(CommandStart())
async def bot_start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}! Чтобы добавить новый расход, выберите категорию.",
                         reply_markup=category_markup())


@dp.message_handler(IsCategory(), state=ExpenseState.category)
@dp.message_handler(IsCategory())
async def set_category(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text
        data['delete_message'] = await message.answer('Отлично! Теперь введите сумму расхода.')
    await message.delete()
    await ExpenseState.expense.set()


@dp.message_handler(state=ExpenseState.expense)
async def set_expense(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['expense'] = message.text
        db.add_expense(message.from_user.id, datetime.today().date(), data['category'], float(data['expense']))
        id = db.get_expenses_by_user(message.from_user.id)[-1][0]
        await message.delete()
        await message.answer(
            f"✅️ Добавлен расход : {data['expense']} ₽ ✅️\nКатегория: {data['category']}\nДата: Сегодня ({str(datetime.today().day)}.{str(datetime.today().month)}.{str(datetime.today().year)})\n📊 Расходы за сегодня: {await get_total_daily_expenses(message.from_user.id)} ₽",
            reply_markup=expense_markup(id))
        await bot.delete_message(message.chat.id, data['delete_message'].message_id)
    await state.finish()


@dp.callback_query_handler(expense_cb.filter(action='add_notes'))
async def add_notes(query: CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = callback_data['id']
        data['message'] = query.message
        data['delete_message'] = await query.message.answer('Напишите комментарий.')
    await NotesState.notes.set()


@dp.message_handler(state=NotesState.notes)
async def notes_submit(message: Message, state: FSMContext):
    user_id = message.from_user.id
    async with state.proxy() as data:
        data['notes'] = message.text
        await message.delete()
        await bot.delete_message(message.chat.id, data['delete_message'].message_id)
        message = data['message']
        id = data['id']
        db.add_notes(id, data['notes'])
        amount, category, notes, day, month, year = await get_expense_values(id)
        await message.edit_text(
            f"✅️ Добавлен расход : {amount} ₽ ✅️\nКатегория: {category}\nДата: Сегодня ({day}.{month}.{year})\nКомментарий: {notes}\n📊 Расходы за сегодня: {await get_total_daily_expenses(user_id)} ₽")
        await message.edit_reply_markup(expense_markup(id))
    await state.finish()


@dp.callback_query_handler(expense_cb.filter(action='delete_expense'))
async def delete_expense(query: CallbackQuery, callback_data: dict):
    id = callback_data['id']
    db.delete_expense(id)
    await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
    await query.message.answer(f'📊 Расходы за сегодня: {await get_total_daily_expenses(query.from_user.id)} ₽',
                               reply_markup=category_markup())
    await query.answer('Расход удален!')


@dp.callback_query_handler(expense_cb.filter(action='edit_date'))
async def edit_date(query: CallbackQuery, callback_data: dict):
    id = callback_data['id']
    await query.message.edit_reply_markup(date_markup(id))


@dp.callback_query_handler(expense_cb.filter(action='choose_day'))
async def choose_day(query: CallbackQuery, callback_data: dict):
    id = callback_data['id']
    await query.message.edit_reply_markup(choose_day_markup(id))


@dp.callback_query_handler(expense_cb.filter(action='set_today'))
async def set_today(query: CallbackQuery, callback_data: dict):
    id = callback_data['id']
    db.update_expense_date(id, datetime.today().date())
    amount, category, notes, day, month, year = await get_expense_values(id)
    if not notes:
        await query.message.edit_text(
            f"✅️ Добавлен расход : {amount} ₽ ✅️\nКатегория: {category}\nДата: Сегодня ({day}.{month}.{year})\n📊 Расходы за сегодня: {await get_total_daily_expenses(query.from_user.id)} ₽")
    else:
        await query.message.edit_text(
            f"✅️ Добавлен расход : {amount} ₽ ✅️\nКатегория: {category}\nДата: Сегодня ({day}.{month}.{year})\nКомментарий: {notes}\n📊 Расходы за сегодня: {await get_total_daily_expenses(query.from_user.id)} ₽")
    await query.message.edit_reply_markup(expense_markup(id))


@dp.callback_query_handler(expense_cb.filter(action='set_yesterday'))
async def set_yesterday(query: CallbackQuery, callback_data: dict, state: FSMContext):
    id = callback_data['id']
    yesterday = datetime.today() - timedelta(days=1)
    db.update_expense_date(id, yesterday.date())
    amount, category, notes, day, month, year = await get_expense_values(id)
    if not notes:
        await query.message.edit_text(
            f"✅️ Добавлен расход : {amount} ₽ ✅️\nКатегория: {category}\nДата: Вчера ({day}.{month}.{year})\n📊 Расходы за сегодня: {await get_total_daily_expenses(query.from_user.id)} ₽")
    else:
        await query.message.edit_text(
            f"✅️ Добавлен расход : {amount} ₽ ✅️\nКатегория: {category}\nДата: Вчера ({day}.{month}.{year})\nКомментарий: {notes}\n📊 Расходы за сегодня: {await get_total_daily_expenses(query.from_user.id)} ₽")
    await query.message.edit_reply_markup(expense_markup(id))


@dp.callback_query_handler(expense_cb.filter(action='set_year'))
async def set_year(query: CallbackQuery, callback_data: dict):
    id = callback_data['id']
    await query.message.edit_reply_markup(set_year_markup(id))


@dp.callback_query_handler(expense_cb.filter(
    action=['set_current_year-0', 'set_current_year-1', 'set_current_year-2', 'set_current_year-3']))
async def handle_callback_query(query: CallbackQuery, state: FSMContext, callback_data: dict):
    selected_year = int(datetime.now().year) - int(query.data.split('-')[-1])
    async with state.proxy() as data:
        data['year'] = int(selected_year)
        id = callback_data['id']
        if 'month' in data.keys() and 'day' in data.keys():
            await query.message.edit_reply_markup(choose_day_markup(id, data['year'], data['month'], data['day']))
        elif 'month' in data.keys() and 'day' not in data.keys():
            await query.message.edit_reply_markup(choose_day_markup(id, year=data['year'], month=data['month']))
        elif 'month' not in data.keys() and 'day' in data.keys():
            await query.message.edit_reply_markup(choose_day_markup(id, year=data['year'], day=data['day']))
        else:
            await query.message.edit_reply_markup(choose_day_markup(id, year=data['year']))


@dp.callback_query_handler(expense_cb.filter(action='set_month'))
async def set_month(query: CallbackQuery, callback_data: dict):
    id = callback_data['id']
    await query.message.edit_reply_markup(set_month_markup(id))


@dp.callback_query_handler(expense_cb.filter(
    action=['choose_month_1', 'choose_month_2', 'choose_month_3', 'choose_month_4', 'choose_month_5', 'choose_month_6',
            'choose_month_7', 'choose_month_8', 'choose_month_9', 'choose_month_10', 'choose_month_11',
            'choose_month_12']))
async def handle_callback_query(query: CallbackQuery, state: FSMContext, callback_data: dict):
    selected_month = int(query.data.split('_')[-1])
    async with state.proxy() as data:
        data['month'] = selected_month
        id = callback_data['id']
        if 'year' in data.keys() and 'day' in data.keys():
            await query.message.edit_reply_markup(choose_day_markup(id, data['year'], data['month'], data['day']))
        elif 'year' in data.keys() and 'day' not in data.keys():
            await query.message.edit_reply_markup(choose_day_markup(id, year=data['year'], month=data['month']))
        elif 'year' not in data.keys() and 'day' in data.keys():
            await query.message.edit_reply_markup(choose_day_markup(id, month=data['month'], day=data['day']))
        else:
            await query.message.edit_reply_markup(choose_day_markup(id, month=data['month']))


@dp.callback_query_handler(expense_cb.filter(action='set_day'))
async def set_day(query: CallbackQuery, callback_data: dict, state: FSMContext):
    id = callback_data['id']
    async with state.proxy() as data:
        if 'year' in data.keys() and 'month' in data.keys():
            await query.message.edit_reply_markup(set_day_markup(id, year=data['year'], month=data['month']))
        elif 'year' in data.keys() and 'month' not in data.keys():
            await query.message.edit_reply_markup(set_day_markup(id, year=data['year']))
        elif 'year' not in data.keys() and 'month' in data.keys():
            await query.message.edit_reply_markup(set_day_markup(id, month=data['month']))
        else:
            await query.message.edit_reply_markup(set_day_markup(id))


@dp.callback_query_handler(expense_cb.filter(
    action=['choose_day_1', 'choose_day_2', 'choose_day_3', 'choose_day_4', 'choose_day_5', 'choose_day_6',
            'choose_day_7', 'choose_day_8', 'choose_day_9', 'choose_day_10', 'choose_day_11',
            'choose_day_12', 'choose_day_13', 'choose_day_14', 'choose_day_15', 'choose_day_16', 'choose_day_17',
            'choose_day_18', 'choose_day_19', 'choose_day_20', 'choose_day_21', 'choose_day_22',
            'choose_day_23', 'choose_day_24', 'choose_day_25', 'choose_day_26', 'choose_day_27', 'choose_day_28',
            'choose_day_29', 'choose_day_30', 'choose_day_31']))
async def handle_callback_query(query: CallbackQuery, state: FSMContext, callback_data: dict):
    selected_day = int(query.data.split('_')[-1])
    async with state.proxy() as data:
        data['day'] = selected_day
        id = callback_data['id']
        if 'year' in data.keys() and 'month' in data.keys():
            await query.message.edit_reply_markup(
                choose_day_markup(id, year=data['year'], month=data['month'], day=data['day']))
        elif 'year' in data.keys() and 'month' not in data.keys():
            await query.message.edit_reply_markup(choose_day_markup(id, year=data['year'], day=data['day']))
        elif 'year' not in data.keys() and 'month' in data.keys():
            await query.message.edit_reply_markup(choose_day_markup(id, month=data['month'], day=data['day']))
        else:
            await query.message.edit_reply_markup(choose_day_markup(id, day=data['day']))


@dp.callback_query_handler(expense_cb.filter(action='accept_day'))
async def accept_day(query: CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        if 'day' in data.keys():
            day = data['day']
        else:
            day = datetime.today().day
        if 'month' in data.keys():
            month = data['month']
        else:
            month = datetime.today().month
        if 'year' in data.keys():
            year = data['year']
        else:
            year = datetime.today().year
        id = callback_data['id']
        try:
            db.update_expense_date(id, datetime(year, month, day).date())
        except ValueError:
            await query.answer("День выходит за пределы диапазона для месяца", show_alert=True)
        amount, category, notes, day, month, year = await get_expense_values(id)
        if not notes:
            await query.message.edit_text(
                f"✅️ Добавлен расход : {amount} ₽ ✅️\nКатегория: {category}\nДата: {day}.{month}.{year}\n📊 Расходы за сегодня: {await get_total_daily_expenses(query.from_user.id)} ₽")
        else:
            await query.message.edit_text(
                f"✅️ Добавлен расход : {amount} ₽ ✅️\nКатегория: {category}\nДата: {day}.{month}.{year}\nКомментарий: {notes}\n📊 Расходы за сегодня: {await get_total_daily_expenses(query.from_user.id)} ₽")
        await query.message.edit_reply_markup(expense_markup(id))
    await state.finish()


@dp.callback_query_handler(expense_cb.filter(action='cancel_choose_day'))
async def cancel_choose_day(query: CallbackQuery, callback_data: dict):
    id = callback_data['id']
    await query.message.edit_reply_markup(expense_markup(id))
