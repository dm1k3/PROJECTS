from atm import ATM
from db import DB

class MainApp:

	def main(self):
		"""Главная функция приложения."""
		FLAG = True
		atm = ATM()

		while FLAG:
			self.show_start_screen()
			answer = input('\nВыберите допустимый пункт меню: ')
			if answer == 1 or answer == '1':
				result = atm.login()
				if result == True:
					print('\nПин-код верен !')
					self.private_office(atm)
				elif result == False:
					print('\nСчет не найден !')
				else:
					print(result)
			elif answer == 2 or answer == '2':
				print(atm.open_account())
			elif answer == 3 or answer == '3':
				print(atm.delete_account())
			else:
				print('\nНедопустимый ввод ! Проверьте верность ввода !')

	def private_office(self, atm):
		"""Функция личного кабинета клиента."""
		FLAG = True
		while FLAG:
			self.show_private_office_menu()
			choice = input('\nВведите пункт меню: ')
			if choice == '1' or choice == 1:
				# Внесение денег на счёт:
				print(atm.depositing_money())
			elif choice == '2' or choice == 2:
				# Снятие денег со счёта:
				print(atm.withdraw_money())
			elif choice == '3' or choice == 3:
				# Перевод денег на счёт:
				print(atm.transfer_money())
			elif choice == '4' or choice == 4:
				# Выводит информацию о счёте:
				atm.show_account_data()
			elif choice == '5' or choice == 5:
				FLAG = False
			else:
				print('\nНедопустимый ввод ! Проверьте корректность ввод !')

	def show_private_office_menu(self):
		"""Выводит меню личного кабинета клиента."""
		print('\nЛичный кабинет пользователя:')
		print('-----------------------------')
		print('1. Внести сумму')
		print('2. Снять наличные.')
		print('3. Перевести деньги.')
		print('4. Информация о счёте.')
		print('5. Выйти.')

	def show_start_screen(self):
		"""Функция представляет собой стартовый экран."""

		print('\nДобро пожаловать в aKBank !')
		print('---------------------------')
		print('1. Войти.')
		print('2. Открыть счёт.')
		print('3. Закрыть счёт.')


if __name__ == '__main__':
	MainApp().main()