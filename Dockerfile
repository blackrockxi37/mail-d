FROM python:3.9-slim

WORKDIR /app

RUN apk add libffi-dev

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]