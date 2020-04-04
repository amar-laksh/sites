set -o nounset                                  # Treat unset variables as an error
#!/bin/bash
# File              : connect.sh
# Author            : Amar Lakshya <amar.lakshya@xaviers.edu.in>
# Date              : 28.08.2019
# Last Modified Date: 30.08.2019
# Last Modified By  : Amar Lakshya <amar.lakshya@xaviers.edu.in>
WARGAME=narnia
PORT=2226
cur=$(echo "$1 - 1" | bc)
if   [[ $# -lt 1  ]] || [[ "$cur" -gt "$(cat $WARGAME/flags | wc -l)" ]]; then
	echo "usage: ./connect.sh level"
	exit 0
fi
echo "So let's go in $WARGAME$cur... to get $WARGAME$1!"
chmod 600 $WARGAME/*.sshkey &> /dev/null
firefox http://overthewire.org/wargames/$WARGAME/$WARGAME$1.html
flag=$(cat $WARGAME/flags | awk -v n=$cur 'FNR == n')
if [[ $(echo $flag | grep -c "ssh") -eq 1 ]]; then
	ssh $WARGAME$cur@$WARGAME.labs.overthewire.org -i "$flag" -p $PORT
else
	sshpass -p "$flag" ssh $WARGAME$cur@$WARGAME.labs.overthewire.org -p $PORT
fi
