#!/bin/bash

# url: http://www.cyberciti.biz/faq/bash-infinite-loop/
while :
do
	rostopic list &> /dev/null
	# url: http://stackoverflow.com/questions/5195607/checking-bash-exit-status-of-several-commands-efficiently
	if [ $? -ne 0 ]; then
		rm -f ~/.powerline-shell.ROS.reachable
	else
		touch ~/.powerline-shell.ROS.reachable
	fi

	sleep 0.5
done