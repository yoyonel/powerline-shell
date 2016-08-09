#!/bin/bash

filename_for_ROS_reachable=~/.powerline-shell.ROS.reachable
filename_for_ROS_topics=~/.powerline-shell.ROS.topics

# url: http://www.cyberciti.biz/faq/bash-infinite-loop/
while :
do
	rostopic list &> $filename_for_ROS_topics

	ROS_reachable=$(expr $? '!=' 0)

	# # url: http://stackoverflow.com/questions/5195607/checking-bash-exit-status-of-several-commands-efficiently
	# if $ROS_reachable ; then
	# 	rm -f $filename_for_ROS_reachable
	# else
	# 	touch $filename_for_ROS_reachable
	# fi

	# nb_topics=$(cat $filename_for_ROS_topics | wc -l)
	# echo $nb_topics > $filename_for_ROS_topics

	msg_json=$(printf '{"reachable":"%s"}{"toto":"tata"}\n' "$ROS_reachable")
	echo $msg_json
	curl -H "Content-Type: application/json" -X POST -d $msg_json http://127.0.0.1:8080/api/v1/addrecord/ros

	sleep 1.0
done