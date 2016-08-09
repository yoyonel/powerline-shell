#!/bin/bash

filename_for_ROS_reachable=~/.powerline-shell.ROS.reachable
filename_for_ROS_topics=~/.powerline-shell.ROS.topics

# url: http://www.cyberciti.biz/faq/bash-infinite-loop/
while :
do
	# url: http://stackoverflow.com/questions/4651437/how-to-set-a-variable-equal-to-the-output-from-a-command-in-bash
	ROS_topics_list=`rostopic list &> /dev/null`
	ROS_reachable=`expr $? '!=' 1`
	# echo $ROS_reachable
	# url: http://tldp.org/LDP/Bash-Beginners-Guide/html/sect_07_01.html
	if [ $ROS_reachable -ne 0 ]; then
		ROS_topics_counter=`rostopic list | wc -l`
		# echo ROS_topics_counter: $ROS_topics_counter
		# echo ROS_topics_list: $ROS_topics_list
	else
		ROS_topics_counter=0
	fi

	# # url: http://stackoverflow.com/questions/5195607/checking-bash-exit-status-of-several-commands-efficiently
	# if $ROS_reachable ; then
	# 	rm -f $filename_for_ROS_reachable
	# else
	# 	touch $filename_for_ROS_reachable
	# fi

	# requete curl pour sauvegarder les infos
	# url: http://stackoverflow.com/questions/17029902/using-curl-post-with-variables-defined-in-bash-script-functions
	curl -H "Content-Type: application/json" -X POST \
		--data '{"reachable":"'"$ROS_reachable"'","topics":"'"$ROS_topics_counter"'"}'  \
		http://127.0.0.1:8080/api/v1/addrecord/ros

	sleep 1.0
done