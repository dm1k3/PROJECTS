from db import DB
from datetime import datetime
from argon2 import PasswordHasher

class ATM:

	def __init__(self):
		self.name = ''
		self.account = 0
		self.reg_date = ''
		self.password = ''
		self.balance = 0

	def login(self):
		userAccount = int(input('\nВведите номер вашего счёта: '))
		info_account = DB(userAccount).search_account()
		if info_account == False:
			return False

		self.name, self.account, self.reg_date, self.password, self.balance = info_account
		user_passwd = self.verify_password()
		if user_passwd == True:
			return True
		else:
			return '\nПин-код неверен !'

	def open_account(self):
		fullname, password, num_account, balance = self.enter_date()

		print('\nПроверка данных: ')
		print(f'Имя: {fullname}')
		print(f'Номер счёта: {num_account}')
		confirm = input('\nВведенные данные верны "да"("yes")/"нет"("no"): ')
		if confirm == 'да' or confirm == 'yes':
			reg_date = self.get_date()
			password = PasswordHasher().hash(password)
			# Запись в БД
			DB().entry_db(fullname, num_account, password, balance, reg_date)
			return '\nВаш счёт открыт !'
		else:
			return '\nПользователь отменил открытие !'

	def delete_account(self):
		user_account = int(input('\nВведите номер счета, который хотите закрыть: '))
		found_account = DB(user_account).search_account()
		if found_account == False:
			return '\nНомер счета не найден !'

		self.name, self.account, self.reg_date, self.password, self.balance = found_account
		confirm = input(f'Хотите удалить счет {self.account}, владелец: {self.name} (yes, да)/(no, нет): ')
		if confirm == 'yes' or confirm == 'да':
			check = self.verify_password()
			if check == True:
				DB(self.account).delete_account()
				return '\nСчёт успешно закрыт !'
			else:
				return '\nПроверка при закрытии счета не пройдена ! Введен неверный пин-код !'
		elif confirm == 'no' or confirm == 'нет':
			return '\nОперация закрытия счёта отменена !'
		else:
			return '\nНедопустимый ввод !'

	def depositing_money(self):
		money = int(input('Введите целочисленную сумму пополнения счета: '))
		if money < 0:
			money = int(input('Неверный ввод суммы ! Введите сумму по новой: '))
		elif money == 0:
			return 'Нельзя пополнить счёт на нулевую сумму !'

		self.balance += money
		DB(self.account).changing_balance(self.balance)
		return 'Счет успешно пополнен !'

	def withdraw_money(self):
		money = float(input('Введите целочисленную сумму для снятия: '))

		if money > self.balance:
			return 'Недостаточно средств на счёте !'
		elif money == 0:
			return 'Нельзя снять нулевую сумму со счёта !'

		self.balance -= money
		DB(self.account).changing_balance(self.balance)
		return 'Сумма успешно снята !'

	def transfer_money(self):
		transfer_account = int(input('Введите номер счета клиента для перевода: '))
		transfer_account_info = DB(transfer_account).search_account()
		if transfer_account_info == False:
			return f'Счёт №{transfer_account} не найден !'
		name_client = transfer_account_info[0]
		balance_client = transfer_account_info[4]
		confirm = input(f'Хотите перевести деньги на счёт {name_client} (yes, да)/(no, нет): ')
		if confirm == 'yes' or confirm == 'да':
			money = float(input(f'Введите сумму для перевода на счёт {name_client}: '))
			if money > self.balance:
				return 'Недостаточно средств на вашем счёте !'
			elif money == 0:
				return 'Нельзя перевести нулевую сумму !'
			elif money < 0:
				return 'Нельзя перевести отрицательную сумму !'
			self.balance -= money
			DB(self.account).changing_balance(self.balance)
			balance_client += money
			DB(transfer_account).changing_balance(balance_client)
			return f'Сумма успешно переведена на счёт {name_client} !'
		elif confirm == 'no' or confirm == 'нет':
			return 'Операция перевода отменена пользователем !'
		else:
			return 'Неверный ввод для подтверждения операции !'

	def enter_date(self):
		first_name = input('\nВведите ваше имя: ')
		last_name = input('Введите вашу фамилию: ')
		middle_name = input('Введите ваше отчество: ')
		fullname = self.verify_name(first_name, last_name, middle_name)
		passwd = self.create_passwd()
		num_account = DB().get_last_num_account()
		balance = 0

		return fullname, passwd, num_account + 1, balance

	def verify_name(self, first_name, last_name, middle_name):
		if middle_name == '':
			return f'{first_name} {last_name}'
		else:
			return f'{first_name} {last_name} {middle_name}'

	def create_passwd(self):
		passwd = input('\nВведите 4-значный пин-код: ')
		while len(passwd) < 4 or len(passwd) > 4:
			print('Пин-код неверен ! Проверьте корректность пин-кода: ')
			passwd = input('Введите пин-код ещё раз: ')

		return passwd

	def verify_password(self):
		user_passwd = input('\nВведите 4-значный пин-код: ')
		try:
			return PasswordHasher().verify(self.password, user_passwd)
		except:
			return False

	def show_account_data(self):
		print('\nИнформация о счёте:')
		print('----------------------------------')
		print(f'Имя владельца счёта: {self.name}')
		print(f'Номер счёта: {self.account}')
		print(f'Дата открытия: {self.reg_date}')
		print(f'Баланс счёта: {self.balance}')

	@classmethod
	def get_date(cls):
		return datetime.now().strftime("%d.%m.%Y")
