from argon2 import PasswordHasher
import pyAesCrypt
import sqlite3 
import os


def main():
	name = get_name_db()

	heading()
	print('Программа завершена.')


def part_login():
	"""Функция выполняет вход в учётную запись приложения."""

	heading()
	try:
		name = input('Введите имя пользователя: ')
		password = get_password(name)

		if password == False:
			heading()
			print(f'Учетная запись с именем {name} не найдена !')
		else:
			user_password = input('Введите пароль: ')

			# Проверяем, соответствует ли пользовательский ввод хешированному паролю
			result = verification_passwd(password, user_password)
			if result == True:
				heading()
				print('Пароль верен !')
				part_client_room(name)
			else:
				heading()
				print('Пароль неверен !')
	except KeyboardInterrupt:
		message_keyboard_interrupt()


def part_client_room(name):
	"""Функция пользовательской комнаты."""
	FLAG = True
	
	while FLAG:
		show_menu_client_room(name)
		try:
			choice = int(input('\nВведите пункт меню: '))
		except ValueError:
			heading()
			print('Неверно указан пункт меню !')
			continue
		except KeyboardInterrupt:
			heading()
			print('Неверно указан пункт меню !')
			continue

		if choice == 1:
			encrypt_file()
		elif choice == 2:
			decrypt_file()
		elif choice == 3:
			FLAG = False
		else:
			heading()
			print('Неверно указан пункт меню !')
			continue


def show_menu_client_room(name):
	"""Меню пользовательской комнаты."""
	heading()
	print(f'Личный кабинет пользователя {name}:')
	print('--------------------------------------------')
	print('1. Зашифровать текстовый файл.')
	print('2. Расшифровать текстовый файл.')
	print('3. Закрыть приложение.')


def encrypt_file():
	"""Функция шифрует текстовые файлы."""

	heading()
	print('ПРИМЕЧАНИЕ !!! ПРИ ШИФРОВАНИИ ФАЙЛА ОРИГИНАЛЬНЫЙ ФАЙЛ УДАЛЯЕТСЯ !!!' \
		  'ПРИ НЕОБХОДИМОСТИ РЕКОМЕНДУЕТСЯ СДЕЛАТЬ КОПИЮ ОРИГИНАЛА !!!')

	heading()
	try:
		user_path = input('Введите путь к файлу: ')
	
		user_file = user_path.split('\\')[-1]	
		enfile = f'{user_file}.aes'

		password = input('Введите пароль для файла: ')
		hashed_password = hashing_passwd(password)
	
		with open(user_path, 'rb') as f:
			with open(enfile, 'wb') as enf:
				pyAesCrypt.encryptFile(user_path, enfile, password)

		heading()
		print(f'Файл успешно зашифрован !')
		os.remove(user_path)
	except FileNotFoundError:
		heading()
		print(f'Не удается найти путь: {user_path} !')
	except KeyboardInterrupt:
		message_keyboard_interrupt()


def decrypt_file():
	"""Функция расшифровывает текстовые файлы."""

	heading()
	print('ПРИМЕЧАНИЕ !!! ПРИ ДЕШИФРОВАНИИ ФАЙЛА ЗАШИФРОВАННЫЙ ФАЙЛ УДАЛЯЕТСЯ !!!' \
		  'ПРИ НЕОБХОДИМОСТИ РЕКОМЕНДУЕТСЯ СДЕЛАТЬ КОПИЮ !!!')
	
	heading()
	try:
		encrypt_file = input('Введите название зашифрованного файла: ')
		decrypt_file = encrypt_file[:-4]
	
		with open(encrypt_file, 'rb') as enfile:
			with open(decrypt_file, 'wb') as file:
				user_password = input(f'Введите пароль для файла {encrypt_file}: ')
				pyAesCrypt.decryptFile(encrypt_file, decrypt_file, user_password)
				heading()
				print('Файл успешно расшифрован !')

		os.remove(encrypt_file)
	except FileNotFoundError:
		heading()
		print(f'Файл {encrypt_file} не найден !')
	except ValueError:
		heading()
		print(f'Неверный пароль для {encrypt_file} !')
		os.remove(decrypt_file)
	except KeyboardInterrupt:
		message_keyboard_interrupt()


def get_password(name):
	"""Функция получает пароль из БД, если имя пользователя найдено в БД."""

	conn = sqlite3.connect('user.db')
	cur = conn.cursor()

	try:
		cur.execute('''SELECT Password FROM User WHERE Name = ?''', (name,))
	except sqlite3.OperationalError:
		create_user_db()

	passwd = cur.fetchone()

	if passwd is None: 
		return False
	else:
		return passwd[0]


def part_create_account():
	"""Функция создания аккаунта."""

	heading()
	try:
		name = input('Введите имя пользователя: ')
		passwd = input('Введите пароль: ')
		conf_passwd = input('Повторите пароль: ')
	except KeyboardInterrupt:
		message_keyboard_interrupt()

	if passwd == conf_passwd:
		passwd = hashing_passwd(passwd)
		save_account(name, passwd)
		heading()
		print('Аккаунт успешно создан !')
		part_client_room(name)
	else:
		heading()
		print('Пароли не совпадают !')


def hashing_passwd(passwd):
	"""Функция хеширует пароль пользователя."""

	# Создаем экземпляр объекта PasswordHasher
	ph = PasswordHasher()
	passwd = ph.hash(passwd)

	return passwd


def save_account(name, passwd):
	"""Функция сохраняет аккаунт пользователя в БД."""

	conn = sqlite3.connect('user.db')
	cur = conn.cursor()

	try:
		cur.execute('''INSERT INTO User (Name, Password)
				   	   VALUES (?, ?)''', (name, passwd))
	except sqlite3.OperationalError:
		create_user_db()

	conn.commit()
	conn.close()


def create_user_db():
	"""Функция создает БД при её отсутствии."""

	conn = sqlite3.connect('user.db')
	cur = conn.cursor()

	cur.execute('''CREATE TABLE IF NOT EXISTS User (Name TEXT,
													Password TEXT)''')

	conn.commit()
	conn.close()


def get_name_db():
	"""Проверка на имеющийся аккаунт. Если нет, тогда предлагается создать аккаунт."""

	conn = sqlite3.connect('user.db')
	cur = conn.cursor()
	
	try:
		cur.execute('''SELECT Name FROM User''')
	except sqlite3.OperationalError:
		create_user_db()

	name = cur.fetchone()

	if name is None:
		heading()
		print('Учетная запись не создана !')
		part_create_account()
	else:
		part_login()


def verification_passwd(password, user_password):
	"""Функция проверяет, что пароли совпадают."""

	# Создаем экземпляр объекта PasswordHasher
	ph = PasswordHasher()

	# Проверяем, соответствует ли пользовательский ввод хешированному паролю
	try:
		return ph.verify(password, user_password)	
	except Exception as e:
		return False


def heading():
	"""Заголовок для вывода."""

	print('\n\t\tCpytographer')
	print('--------------------------------------------')


def message_keyboard_interrupt():
	heading()
	print('Неверно указаны данные !')



if __name__ == '__main__':
	main()