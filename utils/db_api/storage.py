import sqlite3


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

    def add_expense(self, user_id, date, category, amount, notes):
        self.cursor.execute('''
            INSERT INTO expenses (user_id, date, category, amount, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, date, category, amount, notes))
        self.connect.commit()

    def get_expenses_by_user(self, user_id):
        self.cursor.execute('SELECT * FROM expenses WHERE user_id = ?', (user_id,))
        return self.cursor.fetchall()

    def close_connection(self):
        self.connect.close()
