# PowerLine bash

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
    _launch_daemon_ros
}

# PowerLineShell

# PATH
# export PLS_PATH=/home/latty/Prog/powerline/powerline-shell

# Vars for Daemon ROS
export PLS_DAEMON_ROS_LAUNCHED=0
export DAEMON_ROS_BASH_FILE=$PLS_PATH/ros/daemon_ros.sh
# Config pour HTTP Server
export no_proxy=$no_proxy,localhost,127.0.0.1

source $PLS_PATH/bashrc/launch_http_server.sh
source $PLS_PATH/bashrc/launch_daemon_ros.sh
source $PLS_PATH/bashrc/launch_daemon_docker.sh

# HTTPSERVER configuration
_launch_httpserver

# Daemon Docker for PLS
_launch_daemon_docker

export PROMPT_COMMAND="_update_ps1"