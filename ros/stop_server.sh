#!/bin/bash
HTTPSERVER_PYTHON_FILE=http_server.py
HTTPSERVER_PORT=8080
# url: http://stackoverflow.com/questions/12647196/how-do-i-shut-down-a-python-simplehttpserver
kill -9 `ps -ef |grep $HTTPSERVER_PYTHON_FILE |grep $HTTPSERVER_PORT |awk '{print $2}'`