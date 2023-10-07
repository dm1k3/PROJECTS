import sqlite3
from datetime import datetime

FLAG = True

def main():
	"""Главная функция."""

	while FLAG == True:
		show_start_screen()
		answer = int(input('\nВыберите пункт меню: '))

		if answer == 1:
			part_login()
		elif answer == 2:
			part_open_account()
		elif answer == 3:
			part_delete_account()
		elif answer < 1 or answer > 3:
			answer = int(input('Выберите допустимый пункт меню: '))


def show_start_screen():
	"""Стартовый экран."""

	print('\nДобро пожаловать в aKBank !')
	print('---------------------------')
	print('1. Войти.')
	print('2. Открыть счёт.')
	print('3. Закрыть счёт.')


def part_login():
	"""Авторизация клиента банка."""

	print('\n---------------------------')
	print('Страница авторизации:')
	print('---------------------------')
	user_account = int(input('Введите номер вашего счёта: '))

	info_account = search_info_account(user_account)[0]
	fullname, account, reg_date, password, balance = info_account
	
	verific = passwd_verification(password)

	if verific == True:
		choice = ''
		while choice != 5:
			choice = show_menu_pers_acc(fullname)
			if choice == 1:
				deposit_amount(account)
			elif choice == 2:
				withdraw_cash(account)
			elif choice == 3:
				send_cash(account)
			if choice == 4:
				show_info_account(fullname, account, reg_date)
			elif choice == 5:
				main()
			elif choice > 5:
				print('\n-------------------------------------')
				print(f'Личный кабинет клиента {fullname}:')
				print('-------------------------------------')
				print('Выберите доступную функцию !')
				choice = show_menu_pers_acc(fullname)
	else:
		print('\nСлишком много неудачных попыток входа ! Попробуйте в другой раз !')

def part_delete_account():

	messages_for_part_delete()
	del_account = int(input('Введите счет, который хотите закрыть: '))

	conn = sqlite3.connect('cards.db')
	cur = conn.cursor()

	cur.execute('''SELECT Name, Num_account, Password FROM Cards
				   WHERE Num_account = ?''',
				   (del_account,))
	search = cur.fetchone()

	if search == []:
		messages_for_part_delete()
		print(f'Счета с номером: {account} не существует !')
	else:
		name, account, password = search
		res = passwd_verification(password)
		if res == True:
			messages_for_part_delete()
			confirmation = input(f'Вы действительно хотите удалить счет {name} ?(y/n): ')
			if confirmation == 'y':
				messages_for_part_delete()
				confirmation2 = input(f'Перед удаление выведите все деньги со счёта {account} ! Продолжить (y/n): ')
				if confirmation2 == 'y':
					cur.execute('''DELETE FROM Cards WHERE Num_account == ?''', (account,))
					messages_for_part_delete()
					print(f'Счет клиента {name} номер {account} успешно удален !')
					conn.commit()
					conn.close()
				elif confirmation2 == 'n':
					main()
			elif confirmation == 'n':
				main()
		else:
			messages_for_part_delete()
			print('Слишком много неудачных попыток ! Попробуйте в другой раз !')

def show_menu_pers_acc(fullname):
	"""Выводит меню личного кабинета и предоставляет ввести пункт меню."""

	print('\n-------------------------------------')
	print(f'Личный кабинет клиента {fullname}:')
	print('-------------------------------------')
	print('Доступные функции:')
	print('-------------------------------------')
	print('1. Внести сумму')
	print('2. Снять наличные.')
	print('3. Перевести деньги.')
	print('4. Информация о счёте.')
	print('5. Выйти.')

	choice = int(input('\nВыберите функцию: '))

	return choice

def deposit_amount(account):
	"""Внести сумму."""

	balance = get_balance(account)
	
	print(f'\nПополнение счёта № {account}:')
	print('--------------------------------')
	money = float(input('Введите сумму для пополнения: '))

	if money < 0:
		print('\nНельзя положить на счёт отрицательную сумму !')
		money = float(input('Введите допустимую сумму: '))
	elif money == 0:
		print('\nНевозможно ввести ноль на счёт !')
		money = float(input('Введите допустимую сумму: '))
	elif money == 'exit':
		print('Вы успешно вышли из операции.')
	else:
		balance += money

		update_balance(balance, account)
	
	print(f'\nСумма: {money} руб. зачислена на счёт ! Баланс доступен в информации о счёте.')


def get_balance(account):
	"""Функция получает значение баланса из базы данных."""

	conn = sqlite3.connect('cards.db')
	cur = conn.cursor()

	cur.execute('''SELECT Balance FROM Cards
				   WHERE Num_account = ?''',
				   (account,))

	balance = cur.fetchone()[0]

	return balance


def update_balance(balance, account):
	"""Функция вносит в базу данных изменения баланса счёта."""

	conn = sqlite3.connect('cards.db')
	cur = conn.cursor()

	cur.execute('''UPDATE Cards
				   SET Balance = ?
				   WHERE Num_account == ?''',
				   (balance, account))
	conn.commit()
	conn.close()


def withdraw_cash(account):
	"""Функция снятия наличных."""

	balance = get_balance(account)

	messages_for_withdraw_cash(account)
	money = float(input('Введите сумму для снятия: '))

	if money > balance:
		messages_for_withdraw_cash(account)
		print('Недостаточно средств !')
	elif money == 0:
		messages_for_withdraw_cash(account)
		print('Нельзя снять нулевую сумму !')
		withdraw_cash(balance, account)
	elif money < 0:
		messages_for_withdraw_cash(account)
		print('Нельзя снять отрицательную сумму !')
		withdraw_cash(balance, account)
	else:
		balance -=  money

		update_balance(balance, account)

	messages_for_withdraw_cash(account)
	print(f'Сумма: {money} руб. успешно снята ! Баланс доступен в информации о счёте.')


def send_cash(account):
	"""Перевести деньги."""
	
	my_balance = get_balance(account)

	messages_for_send_cash()
	people_account = int(input('Введите счёт, на который хотите перевести деньги: '))
	info_account = search_people_account(people_account)

	if info_account == []:
		messages_for_send_cash()
		print(f'Номер счёта {people_account} не найден ! \
				\nПроверьте номер введенного счёта и попробуйте ещё раз!')
	else:
		fullname, people_balance = info_account[0]

		messages_for_send_cash()
		confirmation = input(f'Вы хотите перевести деньги на счёт {fullname} ? (y/n): ')
		if confirmation == 'y':
			messages_for_send_cash()
			money = float(input('Введите сумму для перевода: '))

			if money < 0:
				messages_for_send_cash()
				print('Нельзя перевести отрицательную сумму !')
				money = float(input('Введите сумму для перевода ещё раз: '))
			elif money == 0:
				messages_for_send_cash()
				print('Нельзя перевести сумму, которая равна 0 !')
				money = float(input('Введите сумму для перевода ещё раз: '))
			elif money > my_balance:
				messages_for_send_cash()
				print('Недостаточно средств на вашем счёте для перевода денег !')
			else:
				my_balance -= money
				update_balance(my_balance, account)
				people_balance += money
				update_balance(people_balance, people_account)

				messages_for_send_cash()
				print(f'Деньги успешно переведены на счёт {fullname} !')


def search_people_account(people_account):
	"""Функция ищет имя человека и счёт, на который нужно перевести деньги."""

	conn = sqlite3.connect('cards.db')
	cur = conn.cursor()

	cur.execute('''SELECT Name, Balance FROM Cards
				   WHERE Num_account = ?''',
				   (people_account,))

	people_info_account = cur.fetchall()
	return people_info_account


def show_info_account(fullname, account, reg_date):
	"""Показать информацию о клиенте."""

	conn = sqlite3.connect('cards.db')
	cur = conn.cursor()

	cur.execute('''SELECT Balance FROM Cards
		           WHERE Num_account = ?''',
		           (account,))

	balance = cur.fetchone()[0]

	print('\n--------------------------------------')
	print('Информация о счёте клиента в aKBank:')
	print('--------------------------------------')
	print(f'Имя клиента: {fullname}.')
	print(f'Номер счёта: {account}.')
	print(f'Дата открытия: {reg_date}.')
	print(f'БАЛАНС: {balance} рублей.')


def part_open_account():
	"""Открытие счета в банке."""

	NUM_ACCOUNT = 1

	messages_for_open_account()
	first_name = input('Введите ваше имя: ')
	last_name = input('Введите вашу фамилию: ')
	password = int(input('Создайте пин-код из 4 цифр: '))
	fullname = f'{first_name} {last_name}'
	balance = 0

	conn = sqlite3.connect('cards.db')
	cur = conn.cursor()

	try:
		cur.execute('''SELECT Num_account FROM Cards''')
	except Exception as e:
		create_db_table()

	check_accounts = []
	list_accounts = cur.fetchall()
	for acc in list_accounts:
		acc = acc[0]
		check_accounts.append(acc)
	
	if NUM_ACCOUNT in check_accounts:
		NUM_ACCOUNT = check_accounts[-1] + 1
	
	account = NUM_ACCOUNT
	
	messages_for_open_account()
	print(f'Ваше полное имя: {first_name} {last_name}.')
	print(f'Ваш номер счёта: {account}.')
	print('Баланс счёта: 0 руб.')

	confirmation = input('\nДанные верны (y/n) ?: ')
	if confirmation == 'y':
		registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		cur.execute('''INSERT INTO Cards (Name, Num_account, Reg_date, Password, Balance)
					   VALUES (?, ?, ?, ?, ?)''',
					   (fullname, account, registration_date, password, balance))
		conn.commit()
		conn.close()
		messages_for_open_account()
		print('Ваш счет успешно открыт !')
	else:
		part_open_accaunt()


def search_info_account(user_account):
	"""Поиск информации о счёте."""

	conn = sqlite3.connect('cards.db')
	cur = conn.cursor()

	try:
		cur.execute('''SELECT Name, Num_account, Reg_date, Password, Balance 
					   FROM Cards WHERE Num_account = ?''', 
					   (user_account,))
	except Exception as e:
		create_db_table()
	
	account_info = cur.fetchall()

	if account_info == []:
		print('\nВаш счет не найден !')
		answer = input('Хотите открыть счёт (y/n)?: ')

		if answer == 'y':
			part_open_account()
		elif answer == 'n':
			main()
	else:
		return account_info


def create_db_table():
	"""Создание базы данных."""
	conn = sqlite3.connect('cards.db')
	cur = conn.cursor()

	cur.execute('''CREATE TABLE IF NOT EXISTS Cards (ID INTEGER PRIMARY KEY,
													 Name TEXT,
													 Num_account INTEGER,
													 Reg_date TEXT,
													 Password INTEGER,
													 Balance REAL)''')
	conn.commit()
	conn.close()


def passwd_verification(password):
	"""Проверка пин-кода."""

	attempt = 0
	user_input = int(input('\nВведите пин-код: '))
	while True:
		attempt += 1
		if user_input != password and attempt < 3:
			user_input = int(input('Пин-код неверен ! Введите ещё раз пин-код: '))
		elif user_input != password and attempt >= 3:
			return False
		elif password == user_input:
			return True
	
def messages_for_part_delete():
	"""Сообщения, используемые в функции part_delete_account()."""
	print('\n--------------------------------------')
	print('Удаление счета клиента:')
	print('--------------------------------------')

def messages_for_withdraw_cash(account):
	"""Сообщения, используемые в функции withdraw_cash()."""
	print(f'\nСнятие наличных со счёта № {account}:')
	print('-----------------------------')

def messages_for_send_cash():
	"""Сообщения, используемые в функции send_cash()."""
	print('\nПеревод денег на счёт:')
	print('-------------------------------------------------')

def messages_for_open_account():
	"""Сообщения, используемые в функции part_open_account()."""
	print('\n----------------------------------')
	print('Страница открытия счёта клиента:')
	print('----------------------------------')


if __name__ == '__main__':
	main()
