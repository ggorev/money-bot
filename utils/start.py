from datetime import datetime

from loader import db


async def get_total_daily_expenses(user_id, day=datetime.today().date()):
    total_expenses = db.get_total_daily_expenses(user_id, day)
    return round(total_expenses, 2) if total_expenses else 0


async def get_expense_values(id):
    expense = db.get_expenses_by_id(id)
    amount = expense[4]
    category = expense[3]
    notes = expense[5]
    day = expense[2].split('-')[2]
    month = expense[2].split('-')[1]
    year = expense[2].split('-')[0]
    return amount, category, notes, day, month, year
