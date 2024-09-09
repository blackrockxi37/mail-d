FROM python:3.9-slim

# Обновляем пакеты и устанавливаем зависимости, включая libffi-dev
RUN apt-get update && apt-get install -y \
    gcc libc-dev linux-headers libffi-dev postgresql-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Python пакеты
RUN pip install --upgrade pip && pip install --no-cache-dir -r /requirements.txt

# Команда по умолчанию
CMD ["python", "main.py"]
