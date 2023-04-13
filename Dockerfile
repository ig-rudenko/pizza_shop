FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip --no-cache-dir && pip install psycopg2-binary && pip install -r requirements.txt --no-cache-dir;

COPY . .

EXPOSE 8000
