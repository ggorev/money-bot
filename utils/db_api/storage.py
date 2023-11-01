import sqlite3
from datetime import datetime


class ExpensesDB:
    def __init__(self, db_name='expenses.db'):
        self.db_name = db_name
        self.connect = sqlite3.connect(self.db_name)
        self.cursor = self.connect.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date DATE,
                category TEXT,
                amount REAL,
                notes TEXT
            )
        ''')
        self.connect.commit()

    def add_expense(self, user_id, date, category, amount, notes=''):
        self.cursor.execute('''
            INSERT INTO expenses (user_id, date, category, amount, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, date, category, amount, notes))
        self.connect.commit()

    def add_notes(self, expense_id, notes):
        self.cursor.execute('''
            UPDATE expenses 
            SET notes = ?
            WHERE id = ?
        ''', (notes, expense_id))
        self.connect.commit()

    def delete_expense(self, expense_id):
        self.cursor.execute('''
            DELETE FROM expenses 
            WHERE id = ?
        ''', (expense_id,))
        self.connect.commit()

    def get_expenses_by_id(self, id):
        self.cursor.execute('SELECT * FROM expenses WHERE id = ?', (id,))
        return self.cursor.fetchone()

    def get_expenses_by_user(self, user_id):
        self.cursor.execute('SELECT * FROM expenses WHERE user_id = ?', (user_id,))
        return self.cursor.fetchall()

    def update_expense_date(self, expense_id, date=datetime.today().date()):
        self.cursor.execute('''
            UPDATE expenses 
            SET date = ?
            WHERE id = ?
        ''', (date, expense_id))
        self.connect.commit()

    def get_total_daily_expenses(self, user_id, day):
        self.cursor.execute('SELECT SUM(amount) FROM expenses WHERE user_id = ? AND date = ?', (user_id, day))
        total_day_expenses = self.cursor.fetchone()[0]
        return total_day_expenses

    def close_connection(self):
        self.connect.close()