FROM python:3.10-slim

WORKDIR /app

ENV DEBIAN_FRONTEND noninteractive
ARG USERNAME=python

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y sudo \
  && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
  && chmod 0440 /etc/sudoers.d/$USERNAME
RUN apt-get install -y --no-install-recommends git wget curl ca-certificates unzip
RUN apt-get clean all && rm -r /var/lib/apt/lists/*

ENV DEBIAN_FRONTEND dialog


RUN pip install --upgrade pip

COPY ./docker/python/requirements.txt /var/docker-python/

RUN pip install -r /var/docker-python/requirements.txt

