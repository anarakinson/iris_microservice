FROM ubuntu:latest

WORKDIR /usr/src/app

EXPOSE 5000

ENV LANG C.UTF-8

RUN apt update

RUN apt install -y redis
RUN apt install -y redis-server
RUN apt install -y python3
RUN apt install -y python3-pip

COPY . /usr/src/app

RUN pip install -r requirements.txt
RUN chmod +x start.sh

CMD ["bash", "start.sh"]
