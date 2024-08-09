# Используем официальный образ Python 3.9 как базовый
FROM python:3.9-slim

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && apt-get clean

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы с зависимостями
COPY requirements.txt /app/

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app/

# Выполняем миграции базы данных и собираем статику
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Указываем порт, который будет использоваться в контейнере
EXPOSE 8000

# Команда по умолчанию для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
