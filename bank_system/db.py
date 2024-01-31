import sqlite3

class DB:

	def __init__(self, account=0):
		self.account = account
		self.conn = sqlite3.connect('cards.db')
		self.cur = self.conn.cursor()

	def search_account(self):
		self.cur.execute("""SELECT Name, Num_account, Reg_date, Password, Balance FROM Cards
							WHERE Num_account = ?""",
							(self.account,))

		info_account = self.cur.fetchall()

		if len(info_account) == 0:
			return False
		else:
			return info_account[0]

	def get_last_num_account(self):
		self.cur.execute("""SELECT Num_account FROM Cards""")
		num_accounts = self.cur.fetchall()
		if len(num_accounts) == 0:
			return 0
		else:
			return num_accounts[-1][-1]

	def entry_db(self, name, num_account, password, balance, reg_date):
		self.cur.execute("""INSERT INTO Cards (Name, Num_account, Reg_date, Password, Balance)
							VALUES (?, ?, ?, ?, ?)""",
							(name, num_account, reg_date, password, balance))

		self.conn.commit()
		self.conn.close()

	def delete_account(self):
		self.cur.execute('''DELETE FROM Cards WHERE Num_account == ?''', (self.account,))
		self.conn.commit()
		self.conn.close()

	def changing_balance(self, new_value):
		self.cur.execute('''UPDATE Cards
							SET Balance = ?
							WHERE Num_account == ?''',
							(new_value, self.account))

		self.conn.commit()
		self.conn.close()
