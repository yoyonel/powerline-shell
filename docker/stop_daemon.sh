#!/bin/bash

DAEMON_PYTHON_FILE=daemon_docker.py
#HTTPSERVER_PORT=8080

# url: http://stackoverflow.com/questions/12647196/how-do-i-shut-down-a-python-simplehttpserver
#kill -9 `ps -ef |grep $HTTPSERVER_PYTHON_FILE |grep $HTTPSERVER_PORT |awk '{print $2}'`

# urls: 
# - http://unix.stackexchange.com/questions/29878/can-i-access-nth-line-number-of-standard-output
# - http://stackoverflow.com/questions/4538253/how-can-i-exclude-one-word-with-grep
# - http://www.cyberciti.biz/tips/grepping-ps-output-without-getting-grep.html
# id_process=`ps -ef | grep "$DAEMON_PYTHON_FILE" | grep -v "grep --colour=auto" | awk '{print $2}' | sed -n 1p`
id_process=`ps -ef | grep "[p]ython $DAEMON_PYTHON_FILE" | awk '{print $2}'`
# echo id_process: $id_process
if [ $id_process ]; then
	echo "daemon_docker.py [STOP]"
	kill -9 $id_process
else
	echo "no daemon_docker found"
fi