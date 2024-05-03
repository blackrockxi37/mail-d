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

prodtype = '0'
if len(sys.argv) > 1:
    prodtype = sys.argv[1]


#some global flags
flag = True
notyflag = False
getMail_status = 0

#telegram bot and imap connection 
bot = tg.TeleBot(token)
imap = imaplib.IMAP4_SSL(imap_server)
imap.login(username, mail_pass)

if prodtype != '0':
    chatid = rockxi
    bot.send_message(rockxi, f'Prodtype: {prodtype}')


#main function that check email and send last mail to tg group
#
#try - except construction is using for catch logout exception
#
#
def getMail():
    flagy = False
    global getMail_status
    

    try:
        a = imap.select('INBOX')[1][0]
    except Exception as e:
        getMail_status = 1
        bot.send_message(rockxi, 'mail exeption : ' + str(e))
        imap.login(username, mail_pass)
        a = imap.select('INBOX')[1][0]
    
    a = str(int(a) - 0)
    res, msg = imap.fetch(a, '(RFC822)')
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
                sendMail(string)
        if "attachment" in content_disposition and flagy:
            filename = part.get_filename()
            if filename:
                if "?UTF-8?B?" in filename:
                    filename = filename.replace("?UTF-8?B?", '')
                    filename = base64.b64decode(filename).decode()
                folder_name = 'mails/' + a
                if not os.path.isdir(folder_name):
                    os.mkdir(folder_name)
                filepath = os.path.join(folder_name, filename)
                open(filepath, "wb").write(part.get_payload(decode=True))
                sendMail('', filepath)

    #fine code =)
    return 'Сообщение отработано!'   


def sendMail(mail, file= False):
    if not file:
        bot.send_message(chat_id = chatid, text = mail)
        print('отправляю сообщение...')
    if file:
        print('отправляю файл...')
        f = open(file, 'rb')
        bot.send_document(chatid, f, timeout=200)
    return 0


def ThreadMailReader():
    global flag , notyflag , getMail_status
    count = 0
    while flag:
        try:
            count += 1
            a = getMail()
            print(f'<{count}> --> , {a}')
        except Exception as e:
            bot.send_message(chat_id=rockxi, text = str(e), disable_notification=notyflag)
            notyflag = True
            getMail_status = 1
        time.sleep(300)
        


@bot.message_handler()
def messahe_handler(message):
    global getMail_status
    if message.chat.id == rockxi:
        if message.text.strip() == 'Reboot':
            os.execv(sys.argv[0], sys.argv)
        bot.send_message(rockxi, f"Работает.\ngetMail()_status = {getMail_status}")
        print(message.from_user.username, ", ", message.chat.id, " : ", message.text.strip())




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

