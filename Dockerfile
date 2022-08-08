FROM python:3.7-buster
# базовый образ

RUN apt update && apt upgrade -y
# обновление пакетов

WORKDIR /usr/src/app
# установка рабочей директории в контейнере

ENV LANG C.UTF-8
# установка языкового стандарта

COPY requirements.txt ./
RUN pip install -r requirements.txt
# копирование и установка зависимостей

COPY . .
# копирование остальных файлов

RUN chmod -x /usr/src/app/start.sh
