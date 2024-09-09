import telebot as tg
import imaplib
import email
from email.header import decode_header
import base64
from datetime import datetime
import threading
import time
import os
import sys
from hiddendata import *
def get_file_extencion(file_path):
# Используем magic для определения MIME-типа файла
    mime = magic.Magic(mime=True)
    mime_type = mime.from_file(file_path)
    
    # Преобразуем MIME-тип в формат расширения файла
    if 'application/pdf' in mime_type:
        return ".pdf:"
    elif 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' in mime_type:
        return ".docx:"
    elif 'text/plain' in mime_type:
        return ".txt:"
    elif 'image/jpeg' in mime_type:
        return ".jpg:"
    # Добавьте другие MIME-типы и расширения по мере необходимости
    else:
        return ".unknown:"

#some global flags
flag = True
notyflag = False


#telegram bot and imap connection 
bot = tg.TeleBot(token)
imap = imaplib.IMAP4_SSL(imap_server)
imap.login(username, mail_pass)

#main function that check email and send last mail to tg group
#
#try - except construction is using for catch logout exception
#
#
def getMail():

    flagy = False

    a = imap.select('INBOX')[1][0]
    a = str(int(a) - 0)

    res, msg = imap.fetch(a, '(RFC822)')

    if res != 'OK':
        bot.send_message(rockxi, 'Result is not OK...')
        imap.login(username, mail_pass)
        return 'Trying to reconnect...'
    msg = email.message_from_bytes(msg[0][1])
    
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding)

    letter_from = msg["Return-path"]
    # blacklist email's check
    for b in blacklist:
        if str(letter_from) == b:
            # banned robot mail bitch !_!
            return "Уведомление от mail.ru."
    letter_from = letter_from.replace('<', '').replace('>','')

    f = open('times.txt', 'r+')
    times = f.readlines()
    time = email.utils.parsedate_tz(msg["Date"])
    messagetime = datetime(time[0],time[1],time[2],time[3],time[4],time[5])

    if str(messagetime) + '\n' in times:
        return "Нет новых сообщений!"
    
    for part in msg.walk():
        content_disposition = str(part.get("Content-Disposition"))
        if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'plain':
            string = base64.b64decode(part.get_payload()).decode()
            
            times = f.readlines()
            if str(messagetime) + '\n' not in times:
                flagy = True
                f.write(str(messagetime) + '\n')
                sendMail(letter_from + '\n' + string)
        if "attachment" in content_disposition and flagy:
            filename = part.get_filename()
            if filename:
                if "?UTF-8?B?" in filename:
                    filename = filename.replace("?UTF-8?B?", '')
                    filename = base64.b64decode(filename).decode()
                folder_name = 'mails/' + a
                if not os.path.isdir(folder_name):
                    os.mkdir(folder_name) 
                filename_format = get_file_extension(filename)
                filepath = os.path.join(folder_name, 'file.'+filename_format, )
                open(filepath, "wb").write(part.get_payload(decode=True))
                sendMail(file = filepath)
                os.remove(filepath)


    return 'Сообщение отработано!'   


def sendMail(mail = '', file=False):

    if not file:
        bot.send_message(chat_id = chatid, text = mail)
        print('отправляю сообщение...')

    if file:
        print('отправляю файл...')
        f = open(file, 'rb')
        bot.send_document(chatid, f, timeout=200)
        time.sleep(5)
    
    return 0


def ThreadMailReader():
    status, responce = imap.noop()
    if status != 'OK':
        bot.semd_message(rockxi, str(status) +'   '+ str(responce))
    global flag , notyflag , getMail_status
    count = 0

    while flag:
        try:
            count += 1
            a = getMail()
            print(f'<{count}> --> , {a}')
            
        except Exception as e:
            if (str(e) == 'command: SELECT => session timeout'):
                restart()
            bot.send_message(chat_id=rockxi, text = str(e), disable_notification=notyflag)
            notyflag = True
            getMail_status = 1
            restart()
        
        time.sleep(500)
        


@bot.message_handler()
def messahe_handler(message):
    global getMail_status
    text = message.text.strip() 
    if message.chat.id == rockxi:
        if text == 'R':
            time.sleep(15)
            restart()
        if text == '?':
            status, responce = imap.noop()
            if status == 'OK':
                bot.send_message(rockxi, 'IMAP is Logined.')
            else:
                bot.send_message(rockxi, 'Failed. IMAP is NOT Logined. Invalid. Suka.')
            return
        bot.send_message(rockxi, f"Работаю.")
        print(message.from_user.username, ", ", message.chat.id, " : ", message.text.strip())

def restart():
    os.execv(sys.executable, ['python'] + sys.argv + ['3'])



t1 = threading.Thread(target=ThreadMailReader, daemon=True)
t1.start() 


try:
    print("Нажмите Ctrl + С чтобы выйти.")
    bot.infinity_polling(20, True)
except KeyboardInterrupt:
    flag = False
    print('Ctrl + C')
    sys.exit(0)
finally:
    bot.send_message(rockxi, "Я умер...")

