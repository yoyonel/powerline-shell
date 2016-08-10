#!/bin/bash
DAEMON_PYTHON_FILE=daemon_docker.py
#HTTPSERVER_PORT=8080
# url: http://stackoverflow.com/questions/12647196/how-do-i-shut-down-a-python-simplehttpserver
#kill -9 `ps -ef |grep $HTTPSERVER_PYTHON_FILE |grep $HTTPSERVER_PORT |awk '{print $2}'`
# url: http://unix.stackexchange.com/questions/29878/can-i-access-nth-line-number-of-standard-output
kill -9 `ps -ef | grep $DAEMON_PYTHON_FILE | awk '{print $2}' | sed -n 1p`