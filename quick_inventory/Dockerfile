FROM python:3.11-alpine

WORKDIR /quick_inventory

# Сначала копируем только requirements.txt, чтобы использовать кеширование Docker
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
