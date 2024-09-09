FROM python:3.9-alpine

WORKDIR /app

RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev

RUN pip3 install --upgrade pip && pip3 install -r /requirements.txt

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]