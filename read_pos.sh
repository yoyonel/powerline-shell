echo -en "\E[6n"
read -sdR CURPOS
CURPOS=${CURPOS#*[}
echo $CURPOS
