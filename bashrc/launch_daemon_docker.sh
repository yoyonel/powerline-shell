#!/bin/bash

function _launch_daemon_docker()
{
  DAEMON_DOCKER_PYTHON_FILE=$PLS_PATH/docker/daemon_docker.py
  id_process=`ps -ef | grep "[p]ython $DAEMON_DOCKER_PYTHON_FILE" | awk '{print $2}'`
  if [ ! $id_process ]; then
    # echo "no daemon_docker found"
    python $DAEMON_DOCKER_PYTHON_FILE &
  fi
}
