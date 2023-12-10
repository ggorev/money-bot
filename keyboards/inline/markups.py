from datetime import datetime, timedelta

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

expense_cb = CallbackData('expense', 'id', 'action')
statistics_cb = CallbackData('statistics', 'id', 'action')

select_range = "🗓️\nВыбрать диапазон"
all_time = "♾️\nВсе время"
select_day = "📅\nВыбрать день"
week = "7️⃣\nНеделя"
today = "1️⃣\nСегодня"
year = "3️⃣6️⃣5️⃣\nГод"
month = "3️⃣1️⃣\nМесяц"


def statistics_markup(id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(select_range, callback_data=statistics_cb.new(id=id, action='select_range')))
    markup.row(InlineKeyboardButton(all_time, callback_data=statistics_cb.new(id=id, action='all_time')),
               InlineKeyboardButton(select_day, callback_data=statistics_cb.new(id=id, action='select_day')))
    markup.row(InlineKeyboardButton(week, callback_data=statistics_cb.new(id=id, action='week')),
               InlineKeyboardButton(today, callback_data=statistics_cb.new(id=id, action='today')))
    markup.row(InlineKeyboardButton(year, callback_data=statistics_cb.new(id=id, action='year')),
               InlineKeyboardButton(month, callback_data=statistics_cb.new(id=id, action='month')))
    return markup


def expense_markup(id):
    global expense_cb
    markup = InlineKeyboardMarkup()
    edit_date = InlineKeyboardButton("🗓 Дата", callback_data=expense_cb.new(id=id, action='edit_date'))
    add_notes = InlineKeyboardButton("💬 Комментарий", callback_data=expense_cb.new(id=id, action='add_notes'))
    markup.row(edit_date, add_notes)
    markup.add(InlineKeyboardButton('🚫 Удалить', callback_data=expense_cb.new(id=id, action='delete_expense')))
    return markup


def date_markup(id):
    global expense_cb
    date = str(datetime.today().date())
    yesterday = str((datetime.today().date() - timedelta(1)).day)
    _, month, day = map(int, date.split('-'))
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября',
              'декабря']
    markup = InlineKeyboardMarkup()
    set_today = InlineKeyboardButton(f"☀️ Сегодня ({str(day) + ' ' + str(months[month - 1])})",
                                     callback_data=expense_cb.new(id=id, action='set_today'))
    set_yesterday = InlineKeyboardButton(f"🌙 Вчера ({yesterday + ' ' + str(months[month - 1])})",
                                         callback_data=expense_cb.new(id=id, action='set_yesterday'))
    markup.add(InlineKeyboardButton('🗓 Выбрать день', callback_data=expense_cb.new(id=id, action='choose_day')))
    markup.add(set_yesterday)
    markup.add(set_today)
    return markup


def choose_day_markup(id, year=int(datetime.now().year), month=int(datetime.now().month), day=int(datetime.now().day),
                      callback=expense_cb):
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября',
              'декабря']
    markup = InlineKeyboardMarkup()
    set_day = InlineKeyboardButton(f"{str(day)}", callback_data=callback.new(id=id, action='set_day'))
    set_month = InlineKeyboardButton(f"{months[month - 1]}", callback_data=callback.new(id=id, action='set_month'))
    set_year = InlineKeyboardButton(f"{str(year)}", callback_data=callback.new(id=id, action='set_year'))
    cancel_choose_day = InlineKeyboardButton('Отменить',
                                             callback_data=callback.new(id=id, action='cancel_choose_day'))
    accept_day = InlineKeyboardButton('Ок', callback_data=callback.new(id=id, action='accept_day'))
    markup.row(set_day, set_month, set_year)
    markup.row(cancel_choose_day, accept_day)
    return markup


def set_year_markup(id, callback=expense_cb):
    year = int(datetime.today().year)
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(f"{str(year - 3)}", callback_data=callback.new(id=id, action='set_current_year-3'))
    button2 = InlineKeyboardButton(f"{str(year - 2)}", callback_data=callback.new(id=id, action='set_current_year-2'))
    button3 = InlineKeyboardButton(f"{str(year - 1)}", callback_data=callback.new(id=id, action='set_current_year-1'))
    button4 = InlineKeyboardButton(f"{str(year)}", callback_data=callback.new(id=id, action='set_current_year-0'))
    markup.row(button4, button3)
    markup.row(button2, button1)
    return markup


def set_month_markup(id, callback=expense_cb):
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября',
              'декабря']
    markup = InlineKeyboardMarkup()
    buttons = []
    for i in range(len(months)):
        button = InlineKeyboardButton(f"{months[i]}",
                                      callback_data=callback.new(id=id, action=f'choose_month_{i + 1}'))
        buttons.append(button)
    markup.row(*buttons[0:4])
    markup.row(*buttons[4:8])
    markup.row(*buttons[8:12])
    return markup


def set_day_markup(id, year=int(datetime.now().year), month=int(datetime.now().month), callback=expense_cb):
    if month in [1, 3, 5, 7, 8, 10, 12]:
        days = list(range(1, 32))
    elif month == 2:
        if year % 4 == 0:
            days = list(range(1, 30))
        else:
            days = list(range(1, 29))
    else:
        days = list(range(1, 31))
    markup = InlineKeyboardMarkup(row_width=7)
    buttons = []
    for i in range(len(days)):
        button = InlineKeyboardButton(f"{days[i]}", callback_data=callback.new(id=id, action=f'choose_day_{i + 1}'))
        buttons.append(button)
    markup.add(*buttons[:7])
    markup.add(*buttons[7:14])
    markup.add(*buttons[14:])
    return markup
