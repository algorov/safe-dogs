FROM python:3.10-slim

# Установка системных зависимостей для opencv
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY . .

# Установка Python-зависимостей
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN ls -R /app

# Указание пути для запуска Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
