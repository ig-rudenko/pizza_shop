FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app

# Для работы с MySQL
RUN apk add --update --no-cache mariadb-connector-c-dev \
	&& apk add --no-cache --virtual .build-deps \
		mariadb-dev \
		gcc \
		musl-dev \
	&& pip install mysqlclient \
	&& apk del .build-deps

RUN pip install --upgrade pip --no-cache-dir && pip install -r requirements.txt --no-cache-dir;

COPY . .

EXPOSE 8000
