FROM ubuntu:latest

# установка рабочей директории
WORKDIR /usr/src/app

# установка рабочего порта внутри контейнера
EXPOSE 5000

# установка рабочего языка
ENV LANG C.UTF-8

# обновление репозиториев контейнера
RUN apt update

# установка необходимого софта
RUN apt install -y redis
RUN apt install -y redis-server
RUN apt install -y python3
RUN apt install -y python3-pip

# копирование файлов приложения внутрь контейнера
COPY . /usr/src/app

# установка зависимостей
RUN pip install -r requirements.txt

# повышение прав скрипта запуска приложения
RUN chmod +x start.sh

# запуск приложения
CMD ["bash", "start.sh"]
