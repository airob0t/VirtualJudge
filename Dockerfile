FROM ubuntu:18.04

MAINTAINER vjudge@vjudge.top

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

#COPY deploy/sources.list /etc/apt/

RUN apt-get update
RUN apt-get install -y python3 python3-pip supervisor nginx
ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
ADD . /app
WORKDIR /app
ADD deploy/nginx.conf /etc/nginx/sites-enabled/default
ADD deploy/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD bash /app/deploy/entrypoint.sh
