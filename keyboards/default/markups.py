from aiogram.types import ReplyKeyboardMarkup


def category_markup():
    markup = ReplyKeyboardMarkup()
    markup.row('🛒 Продукты', '🍴 Кафе')
    markup.row('🎞️ Досуг', '🚍 Транспорт')
    markup.row('⚕️ Здоровье', '🎁 Подарки')
    markup.row('👨‍👩‍👧‍👦 Семья', '🛍️ Покупки')
    return markup
