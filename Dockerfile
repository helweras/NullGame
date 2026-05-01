FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Замените app.py на имя вашего главного файла
CMD ["python", "-u", "game_null.py"]
