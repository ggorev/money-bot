from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.inline import *
from loader import dp, db
from states import StatisticsState
from utils.statistics import get_statistics


@dp.message_handler(commands=['statistics'])
async def statistics(message: Message):
    user_id = message.from_user.id
    await message.delete()
    await message.answer("Выберите период для получения статистики:", reply_markup=statistics_markup(user_id))


@dp.callback_query_handler(statistics_cb.filter(action="select_range"))
async def select_range(query: CallbackQuery, callback_data: dict):
    user_id = callback_data["id"]
    await query.message.delete()
    await query.message.answer("C какой даты?", reply_markup=choose_day_markup(user_id, callback=statistics_cb))
    await StatisticsState.date_from.set()


@dp.callback_query_handler(statistics_cb.filter(action="all_time"))
async def all_time(query: CallbackQuery, callback_data: dict):
    user_id = callback_data["id"]
    expenses = db.get_amount_expenses_all_time(user_id)
    await query.message.delete()
    await query.message.answer(f"{get_statistics(expenses)}")


@dp.callback_query_handler(statistics_cb.filter(action="select_day"))
async def select_day(query: CallbackQuery, callback_data: dict):
    user_id = callback_data["id"]
    await query.message.delete()
    await query.message.answer("Выберите день:", reply_markup=choose_day_markup(user_id, callback=statistics_cb))
    await StatisticsState.select_day.set()


@dp.callback_query_handler(statistics_cb.filter(action="week"))
async def week(query: CallbackQuery, callback_data: dict):
    user_id = callback_data["id"]
    current_date = datetime.now().date()
    start_of_week = current_date - timedelta(days=current_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    expenses = db.get_amount_expenses(user_id, date_from=start_of_week, date_to=end_of_week)
    await query.message.delete()
    await query.message.answer(f"{get_statistics(expenses)}")


@dp.callback_query_handler(statistics_cb.filter(action="today"))
async def today(query: CallbackQuery, callback_data: dict):
    user_id = callback_data["id"]
    current_date = datetime.now().date()
    expenses = db.get_amount_expenses(user_id, current_date, current_date)
    await query.message.delete()
    await query.message.answer(f"{get_statistics(expenses)}")


@dp.callback_query_handler(statistics_cb.filter(action="year"))
async def year(query: CallbackQuery, callback_data: dict):
    user_id = callback_data["id"]
    current_date = datetime.now().date()
    start_of_year = datetime(current_date.year, 1, 1).date()
    end_of_year = datetime(current_date.year, 12, 31).date()
    expenses = db.get_amount_expenses(user_id, date_from=start_of_year, date_to=end_of_year)
    await query.message.delete()
    await query.message.answer(f"{get_statistics(expenses)}")


@dp.callback_query_handler(statistics_cb.filter(action="month"))
async def month(query: CallbackQuery, callback_data: dict):
    user_id = callback_data["id"]
    current_date = datetime.now().date()
    start_of_month = datetime(current_date.year, current_date.month, 1).date()
    end_of_month = datetime(current_date.year, current_date.month, 31).date()
    expenses = db.get_amount_expenses(user_id, date_from=start_of_month, date_to=end_of_month)
    await query.message.delete()
    await query.message.answer(f"{get_statistics(expenses)}")


@dp.callback_query_handler(statistics_cb.filter(action='set_day'), state=StatisticsState.all_states)
async def set_day(query: CallbackQuery, callback_data: dict, state: FSMContext):
    user_id = callback_data['id']
    async with state.proxy() as data:
        if 'year' in data.keys() and 'month' in data.keys():
            await query.message.edit_reply_markup(
                set_day_markup(user_id, year=data['year'], month=data['month'], callback=statistics_cb))
        elif 'year' in data.keys() and 'month' not in data.keys():
            await query.message.edit_reply_markup(set_day_markup(user_id, year=data['year'], callback=statistics_cb))
        elif 'year' not in data.keys() and 'month' in data.keys():
            await query.message.edit_reply_markup(set_day_markup(user_id, month=data['month'], callback=statistics_cb))
        else:
            await query.message.edit_reply_markup(set_day_markup(user_id, callback=statistics_cb))


@dp.callback_query_handler(statistics_cb.filter(action='set_month'), state=StatisticsState.all_states)
async def set_month(query: CallbackQuery, callback_data: dict):
    user_id = callback_data['id']
    await query.message.edit_reply_markup(set_month_markup(user_id, callback=statistics_cb))


@dp.callback_query_handler(statistics_cb.filter(action='set_year'), state=StatisticsState.all_states)
async def set_year(query: CallbackQuery, callback_data: dict):
    user_id = callback_data['id']
    await query.message.edit_reply_markup(set_year_markup(user_id, callback=statistics_cb))


@dp.callback_query_handler(statistics_cb.filter(action='cancel_choose_day'), state=StatisticsState.all_states)
async def cancel_choose_day(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await state.finish()


@dp.callback_query_handler(statistics_cb.filter(
    action=['choose_day_1', 'choose_day_2', 'choose_day_3', 'choose_day_4', 'choose_day_5', 'choose_day_6',
            'choose_day_7', 'choose_day_8', 'choose_day_9', 'choose_day_10', 'choose_day_11',
            'choose_day_12', 'choose_day_13', 'choose_day_14', 'choose_day_15', 'choose_day_16', 'choose_day_17',
            'choose_day_18', 'choose_day_19', 'choose_day_20', 'choose_day_21', 'choose_day_22',
            'choose_day_23', 'choose_day_24', 'choose_day_25', 'choose_day_26', 'choose_day_27', 'choose_day_28',
            'choose_day_29', 'choose_day_30', 'choose_day_31']), state=StatisticsState.all_states)
async def choose_day(query: CallbackQuery, state: FSMContext, callback_data: dict):
    selected_day = int(query.data.split('_')[-1])
    async with state.proxy() as data:
        data['day'] = selected_day
        user_id = callback_data['id']
        if 'year' in data.keys() and 'month' in data.keys():
            await query.message.edit_reply_markup(
                choose_day_markup(user_id, year=data['year'], month=data['month'], day=data['day'],
                                  callback=statistics_cb))
        elif 'year' in data.keys() and 'month' not in data.keys():
            await query.message.edit_reply_markup(
                choose_day_markup(user_id, year=data['year'], day=data['day'], callback=statistics_cb))
        elif 'year' not in data.keys() and 'month' in data.keys():
            await query.message.edit_reply_markup(
                choose_day_markup(user_id, month=data['month'], day=data['day'], callback=statistics_cb))
        else:
            await query.message.edit_reply_markup(choose_day_markup(user_id, day=data['day'], callback=statistics_cb))


@dp.callback_query_handler(statistics_cb.filter(
    action=['choose_month_1', 'choose_month_2', 'choose_month_3', 'choose_month_4', 'choose_month_5', 'choose_month_6',
            'choose_month_7', 'choose_month_8', 'choose_month_9', 'choose_month_10', 'choose_month_11',
            'choose_month_12']), state=StatisticsState.all_states)
async def choose_month(query: CallbackQuery, state: FSMContext, callback_data: dict):
    selected_month = int(query.data.split('_')[-1])
    async with state.proxy() as data:
        data['month'] = selected_month
        user_id = callback_data['id']
        if 'year' in data.keys() and 'day' in data.keys():
            await query.message.edit_reply_markup(
                choose_day_markup(user_id, data['year'], data['month'], data['day'], callback=statistics_cb))
        elif 'year' in data.keys() and 'day' not in data.keys():
            await query.message.edit_reply_markup(
                choose_day_markup(user_id, year=data['year'], month=data['month'], callback=statistics_cb))
        elif 'year' not in data.keys() and 'day' in data.keys():
            await query.message.edit_reply_markup(
                choose_day_markup(user_id, month=data['month'], day=data['day'], callback=statistics_cb))
        else:
            await query.message.edit_reply_markup(
                choose_day_markup(user_id, month=data['month'], callback=statistics_cb))


@dp.callback_query_handler(statistics_cb.filter(
    action=['set_current_year-0', 'set_current_year-1', 'set_current_year-2', 'set_current_year-3']),
    state=StatisticsState.all_states)
async def set_current_year(query: CallbackQuery, state: FSMContext, callback_data: dict):
    selected_year = int(datetime.now().year) - int(query.data.split('-')[-1])
    async with state.proxy() as data:
        data['year'] = int(selected_year)
        user_id = callback_data['id']
        if 'month' in data.keys() and 'day' in data.keys():
            await query.message.edit_reply_markup(
                choose_day_markup(user_id, data['year'], data['month'], data['day'], callback=statistics_cb))
        elif 'month' in data.keys() and 'day' not in data.keys():
            await query.message.edit_reply_markup(
                choose_day_markup(user_id, year=data['year'], month=data['month'], callback=statistics_cb))
        elif 'month' not in data.keys() and 'day' in data.keys():
            await query.message.edit_reply_markup(
                choose_day_markup(user_id, year=data['year'], day=data['day'], callback=statistics_cb))
        else:
            await query.message.edit_reply_markup(choose_day_markup(user_id, year=data['year'], callback=statistics_cb))


@dp.callback_query_handler(statistics_cb.filter(action='accept_day'), state=StatisticsState.date_from)
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
        data.clear()
        user_id = callback_data['id']
        data["date_from"] = datetime(year, month, day).date()
        await query.message.delete()
        await query.message.answer(f"По какую дату?", reply_markup=choose_day_markup(user_id, callback=statistics_cb))
    await StatisticsState.date_to.set()


@dp.callback_query_handler(statistics_cb.filter(action='accept_day'), state=StatisticsState.date_to)
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
        user_id = callback_data['id']
        date_to = datetime(year, month, day).date()
        date_from = data['date_from']
        expenses = db.get_amount_expenses(user_id, date_from=date_from, date_to=date_to)
        await query.message.delete()
        await query.message.answer(f"{get_statistics(expenses)}")
    await state.finish()


@dp.callback_query_handler(statistics_cb.filter(action='accept_day'), state=StatisticsState.select_day)
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
        user_id = callback_data['id']
        date = datetime(year, month, day).date()
        expenses = db.get_amount_expenses(user_id, date, date)
        await query.message.delete()
        await query.message.answer(f"{get_statistics(expenses)}")
    await state.finish()
