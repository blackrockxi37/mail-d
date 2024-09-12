import imaplib
import os
import email
from email.utils import parsedate_to_datetime
from hiddendata import *

def get_lastmail(imap):
    # Получаем список всех папок
    status, folders = imap.list()
    if status != 'OK':
        print("Ошибка при получении списка папок.")
        return None

    last_mail = None
    last_date = None
    last_status = None

    # Итерируемся по каждой папке
    for folder in folders:
        # Получаем информацию о папке
        folder_info = folder.decode()
        try:
            folder_name = folder_info.split(' "/" ')[1].strip('"')
        except IndexError:
            print(f"Ошибка при парсинге имени папки: {folder_info}")
            continue

        # Проверяем, находится ли папка внутри INBOX
        if not folder_name.lower().startswith('inbox'):
            print(f'Пропуск папки, не относящейся к INBOX: {folder_name}')
            continue

        print(f'Переход в папку: {folder_name}')
        
        # Переходим в папку (используем EXAMINE для безопасного режима чтения)
        try:
            status, _ = imap.select(f'"{folder_name}"', readonly=True)  # Проверяем, что имя передается правильно
        except Exception as e:
            print(f"Ошибка при переходе в папку {folder_name}: {e}")
            continue
        
        if status != 'OK':
            print(f"Ошибка при открытии папки {folder_name}.")
            continue

        # Ищем все письма и берем только последнее
        status, messages = imap.search(None, 'ALL')
        if status != 'OK':
            print(f"Ошибка при поиске писем в папке {folder_name}.")
            continue

        # Если писем нет, пропускаем папку
        if not messages[0]:
            continue

        # Берем ID последнего письма
        last_msg_id = messages[0].split()[-1]

        # Получаем данные последнего письма
        status, msg_data = imap.fetch(last_msg_id, '(RFC822)')
        if status != 'OK':
            print(f"Ошибка при получении письма с ID {last_msg_id}.")
            continue

        # Парсинг письма
        msg = email.message_from_bytes(msg_data[0][1])

        # Проверяем наличие даты
        if not msg['Date']:
            print(f"Письмо с ID {last_msg_id} не имеет даты.")
            continue

        msg_date = parsedate_to_datetime(msg['Date'])

        # Сравниваем даты, чтобы найти самое новое письмо
        try:
            if last_date is None or msg_date > last_date:
                last_mail = msg_data
                last_status = status
                last_date = msg_date
        except Exception as e:
            print(f"Ошибка при сравнении дат: {e}. Даты: msg_date={msg_date}, last_date={last_date}")

    # Возвращаем самое новое письмо
    return last_status, last_mail

def get_new_number(path = './mails'):
    items = os.listdir(path)
    nums = [item for item in items if os.path.isdir(os.path.join(path, item))]
    nums = list(map(int, nums))
    nums.sort()
    return str(nums[-1] + 1)