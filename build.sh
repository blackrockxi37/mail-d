#!/bin/bash
echo "Установите предварительно docker"
read -p "Введите почтовый ящик: " username
read -p "Введите пароль от IMAP: " mail_pass
read -p "Введите IMAP сервер: " imap_server
echo 

read -p "Введите chat id (чат группы, куда будут приходить письма): " chatid
read -p "Введите id администратора бота (свой личный): " rockxi
read -p "Введите token от TG бота (выдаёт botFather): " token

cat <<EOL > hiddendata.py
username = "$username"
mail_pass = "$mail_pass"
imap_server = "$imap_server"
chatid = "$chatid"
rockxi = "$rockxi"
token = "$token"
blacklist = [ "<info@e.mail.ru>", "<security@id.mail.ru>" , "<robot@mlrmr.com>" ] 
# blacklist, письма из ящиков, содержащихся в этом массиве не будут пересылаться (не забудь про <> вокруг ящика)
EOL

echo "Данные успешно записаны в hiddendata.py. Теперь соберите docker - контейнер с помощью:\n
        docker build -t mail-d\n
        И запустите с помощью:\n
        docker run -d --restart always mail-d\n
        Чтобы посмотреть ошибки, запусти контейнер без ключа -d"