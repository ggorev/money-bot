from aiogram.types import ReplyKeyboardMarkup

shopping = '🛍️ Покупки'
family = '👨‍👩‍👧‍👦 Семья'
gifts = '🎁 Подарки'
health = '⚕️ Здоровье'
transport = '🚍 Транспорт'
products = '🛒 Продукты'
cafe = '🍴 Кафе'
leisure = '🍿 Досуг'
cancel_expense_message = '🚫 Отменить добавление расхода'
edit_category_message = '✏️ Изменить категорию'
edit_amount_message = '✏️ Изменить сумму расхода'


def category_markup():
    markup = ReplyKeyboardMarkup(is_persistent=True, resize_keyboard=True)
    markup.row(products, cafe)
    markup.row(leisure, transport)
    markup.row(health, gifts)
    markup.row(family, shopping)
    return markup


def cancel_expense_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(cancel_expense_message)
    return markup


def before_add_amount_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Нет')
    markup.add(edit_amount_message)
    markup.add(cancel_expense_message)
    return markup