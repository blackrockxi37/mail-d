# Используем базовый образ с Python
FROM python:3.9-slim

# Устанавливаем libmagic и другие необходимые пакеты
RUN apt-get update && apt-get install -y \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы приложения
COPY . .

# Устанавливаем Python пакеты
RUN pip install --no-cache-dir -r requirements.txt

# Команда по умолчанию
CMD ["python", "main.py"]
