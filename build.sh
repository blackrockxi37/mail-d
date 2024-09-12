#!/bin/bash
echo "U vas doljen bit' ustanovlen docker"
read -p "Введите IMAP сервер: " imap_server
read -p "Введите почтовый ящик: " email
read -s -p "Введите пароль от IMAP: " imap_password
echo 

read -p "Введите chatid: " chatid
read -p "Введите adminid: " rockxi
read -p "Введите token от TG бота: " tg_token

cat <<EOL > hiddendata.py
imap_server = "$imap_server"
username = "$email"
mail_pass = "$imap_password"
chatid = "$chatid"
rockxi = "$adminid"
token = "$tg_token"
blacklist = [ "<info@e.mail.ru>", "<security@id.mail.ru>" , "<robot@mlrmr.com>" ]
EOL

echo "Данные успешно записаны в hiddendata.py"