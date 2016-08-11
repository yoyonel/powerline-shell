#!/bin/bash

function _start_daemon_ros()
{ 
  # echo "_launch_daemon_ros"
  # urls: 
  # - http://superuser.com/questions/150117/how-to-get-parent-pid-of-a-given-process-in-gnu-linux-from-command-line
  # - http://tldp.org/LDP/abs/html/internalvariables.html
  # export SHELLPID=$PPID
  export UPDATEPS1_BASHID=$BASHPID

  # Creation d'un processus detache du parent
  # url: http://linux.101hacks.com/unix/nohup-command/
  nohup /bin/bash $DAEMON_ROS_BASH_FILE &> /dev/null &
  # url: http://unix.stackexchange.com/questions/30370/how-to-get-the-pid-of-the-last-executed-command-in-shell-script
  export DAEMON_ROS_PID=$!
}

function _stop_daemon_ros()
{
  # urls:
  # - http://stackoverflow.com/questions/3043978/how-to-check-if-a-process-id-pid-exists
  # -> http://stackoverflow.com/a/15774758
  # if [ ps -p $DAEMON_ROS_PID &> /dev/null ]; then
  # if [ -e /proc/$DAEMON_ROS_PID ]; then
  if [ -n "$(ps -p $DAEMON_ROS_PID -o pid=)" ]; then
    kill -9 $DAEMON_ROS_PID
    unset DAEMON_ROS_PID
  fi
}

function _launch_daemon_ros()
{
  # urls: 
  # - http://stackoverflow.com/questions/592620/check-if-a-program-exists-from-a-bash-script
  # -> http://stackoverflow.com/a/26759734
  # Est ce que le programme 'roscore' est accessible avec l'env. courant (dans le PATH) ?
  if [ -x "$(command -v roscore)" ]; then
    # -> Si oui [acces au programme 'roscore']    
    # ? A t'on deja lance un demon pour ROS ?
    if [ ! $DAEMON_ROS_PID ]; then
      # -> Si non, on le lance
      # echo "call _launch_daemon_ros"
      _start_daemon_ros
    fi
  else
    # -> Si non [pas acces au programme 'roscore']
    # ? A t'on un daemon ROS actif ? 
    if [ $DAEMON_ROS_PID ]; then
      # -> Si oui, on le desactive
      _stop_daemon_ros
    fi
  fi
}