#!/bin/bash

function _launch_httpserver()
{
  HTTPSERVER_PYTHON_FILE=$PLS_PATH/http_server/http_server.py
  HTTPSERVER_IP=127.0.0.1
  HTTPSERVER_PORT=8080
  id_process=`ps -ef | grep "[p]ython $HTTPSERVER_PYTHON_FILE" | awk '{print $2}'`
  if [ ! $id_process ]; then
    # echo "no daemon_docker found"
    python $HTTPSERVER_PYTHON_FILE $HTTPSERVER_PORT $HTTPSERVER_IP &> /dev/null & 
  fi
}
