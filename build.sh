#!/bin/bash
echo "Установите предварительно docker"
read -p "Введите IMAP сервер: " imap_server
read -p "Введите почтовый ящик: " username
read -p "Введите пароль от IMAP: " mail_pass
echo 

read -p "Введите chatid: " chatid
read -p "Введите adminid: " rockxi
read -p "Введите token от TG бота: " token

cat <<EOL > hiddendata.py
imap_server = "$imap_server"
username = "$username"
mail_pass = "$mail_pass"
chatid = "$chatid"
rockxi = "$rockxi"
token = "$token"
blacklist = [ "<info@e.mail.ru>", "<security@id.mail.ru>" , "<robot@mlrmr.com>" ]
EOL

echo "Данные успешно записаны в hiddendata.py. Теперь соберите docker - контейнер с помощью:
        docker build -t mail-d
        И запустите с помощью:
        docker run -d --restart always mail-d\n"