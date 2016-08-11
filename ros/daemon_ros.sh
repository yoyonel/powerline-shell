#!/bin/bash

# filename_for_ROS_reachable=~/.powerline-shell.ROS.reachable
# filename_for_ROS_topics=~/.powerline-shell.ROS.topics

# urls
# - http://www.cyberciti.biz/faq/bash-infinite-loop/
# - http://tldp.org/LDP/Bash-Beginners-Guide/html/sect_09_02.html
# - http://stackoverflow.com/questions/3043978/how-to-check-if-a-process-id-pid-exists
# -> http://stackoverflow.com/a/15774758
# while ps -p $SHELLPID &> /dev/null;

# => on boucle tant que le bash associe au shell
# qui a lance la creation de ce demon est actif (non tue)
# ps: comme ce daemon est lance a l'aide de nohup
# il n'est pas child du parent (shell/bash), donc quand
# le shell se detruit, il detruit le bash qui ne possede pas cet
# enfant daemon.
# while ps -p $UPDATEPS1_BASHID &> /dev/null;
while [ -n "$(ps -p $UPDATEPS1_BASHID -o pid=)" ];
do
	if [ -x "$(command -v roscore)" ]; then
		# url: http://stackoverflow.com/questions/4651437/how-to-set-a-variable-equal-to-the-output-from-a-command-in-bash
		ROS_topics_list=`rostopic list &> /dev/null`
		ROS_reachable=`expr $? '!=' 1`
		# echo $ROS_reachable
		# url: http://tldp.org/LDP/Bash-Beginners-Guide/html/sect_07_01.html
		if [ $ROS_reachable -ne 0 ]; then
			ROS_topics_counter=`rostopic list | wc -l`
			ROS_nodes_counter=`rosnode list | wc -l`
			################################################
			# [DEBUG]
			# echo ROS_topics_counter: $ROS_topics_counter
			# echo ROS_topics_list: $ROS_topics_list
			################################################
		else
			ROS_topics_counter=0
		fi

		# url: http://unix.stackexchange.com/questions/69322/how-to-get-milliseconds-since-unix-epoch
	 	cur_time=`date +%s%3N`

		# requete curl pour sauvegarder les infos
		# url: http://stackoverflow.com/questions/17029902/using-curl-post-with-variables-defined-in-bash-script-functions
		curl -H "Content-Type: application/json" -X POST \
			--data '{"time":"'"$cur_time"'","reachable":"'"$ROS_reachable"'","topics":"'"$ROS_topics_counter"'","nodes":"'"$ROS_nodes_counter"'"}'  \
			http://127.0.0.1:8080/api/v1/addrecord/ros/$UPDATEPS1_BASHID
		# echo http://127.0.0.1:8080/api/v1/addrecord/ros/$UPDATEPS1_BASHID
	fi

	sleep 1.0
done