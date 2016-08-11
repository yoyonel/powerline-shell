# PowerLine bash
function _launch_daemon_ros()
{ 
  # echo "_launch_daemon_ros"
  # urls: 
  # - http://superuser.com/questions/150117/how-to-get-parent-pid-of-a-given-process-in-gnu-linux-from-command-line
  # - http://tldp.org/LDP/abs/html/internalvariables.html
  export SHELLPID=$PPID
  export UPDATEPS1_BASHID=$BASHPID
  /bin/bash $DAEMON_ROS_BASH_FILE &
  export PLS_DAEMON_ROS_LAUNCHED=1
}

function _stop_daemon_ros()
{
  id_process=`ps -ef | grep "$DAEMON_ROS_BASH_FILE" | grep -v "grep --colour=auto" | awk '{print $2}' | sed -n 1p`
  if [ $id_process ]; then
    kill -9 $id_process
    export PLS_DAEMON_ROS_LAUNCHED=0
  fi
}

function _manage_daemon_ros()
{
  # urls: 
  # - http://stackoverflow.com/questions/592620/check-if-a-program-exists-from-a-bash-script
  # -> http://stackoverflow.com/a/26759734
  if [ -x "$(command -v roscore)" ]; then
    # echo "found roscore"
    # echo "PLS_DAEMON_ROS_LAUNCHED: $PLS_DAEMON_ROS_LAUNCHED"
    # url: http://tldp.org/LDP/abs/html/comparison-ops.html
    if [ $PLS_DAEMON_ROS_LAUNCHED -eq 0 ]; then
      # echo "call _launch_daemon_ros"
      _launch_daemon_ros
    fi
  else
    if [ $PLS_DAEMON_ROS_LAUNCHED -eq 1 ]; then
      _stop_daemon_ros
    fi
  fi
}

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

function _launch_daemon_docker()
{
  DAEMON_DOCKER_PYTHON_FILE=$PLS_PATH/docker/daemon_docker.py
  id_process=`ps -ef | grep "[p]ython $DAEMON_DOCKER_PYTHON_FILE" | awk '{print $2}'`
  if [ ! $id_process ]; then
    # echo "no daemon_docker found"
    python $DAEMON_DOCKER_PYTHON_FILE &
  fi
}

function _update_ps1()
{
  # echo --bash_pid $BASHPID
  # ps: faire attention, $BASHPID doit etre une interpretation
  # du shell, du coup ca peut poser problème a la transmission !
  EVALBASHPID=$BASHPID
  export PS1="$(~/powerline-shell.py --cwd-max-depth 3 --bash_pid $EVALBASHPID $?)" 
  # export PS1="$(~/powerline-shell.py --cwd-max-depth 3 --bash_pid 1234 $?)"
  
  # FOO="$(~/powerline-shell.py ${PREV} --cwd-max-depth 4)"
    # echo ${#FOO[@]}
    # echo $FOO
    # pws_segment_left="$(~/powerline-shell.py ${PREV} --cwd-max-depth 4 --pos_segment left)"
    # pws_segment_right="$(~/powerline-shell.py ${PREV} --cwd-max-depth 4 --pos_segment right)"
    # pws_segment_down="$(~/powerline-shell.py ${PREV} --cwd-max-depth 4 --pos_segment down)"

    # url: http://tldp.org/HOWTO/Bash-Prog-Intro-HOWTO-8.html
    _manage_daemon_ros
}

# PowerLineShell
# PATH
export PLS_PATH=/home/latty/Prog/powerline/powerline-shell
# Vars for Daemon ROS
export PLS_DAEMON_ROS_LAUNCHED=0
export DAEMON_ROS_BASH_FILE=$PLS_PATH/ros/daemon_ros.sh
# Config pour HTTP Server
export no_proxy=$no_proxy,localhost,127.0.0.1

# HTTPSERVER configuration
_launch_httpserver

# Daemon Docker for PLS
_launch_daemon_docker

export PROMPT_COMMAND="_update_ps1"