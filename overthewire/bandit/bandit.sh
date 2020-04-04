set -o nounset                                  # Treat unset variables as an error
#!/bin/bash
# File              : bandit.sh
# Author            : Amar Lakshya <amar.lakshya@xaviers.edu.in>
# Date              : 28.08.2019
# Last Modified Date: 29.08.2019
# Last Modified By  : Amar Lakshya <amar.lakshya@xaviers.edu.in>
cur=$(echo "$1 - 1" | bc)
if   [[ $# -lt 1  ]] || [[ "$cur" -gt "$(cat ./flags | wc -l)" ]]; then
	echo "usage: ./bandit.sh banditnumber"
	exit 0
fi
echo "So let's go in bandit$cur... to get bandit$1!"
chmod 600 ./*.sshkey
firefox http://overthewire.org/wargames/bandit/bandit$1.html
flag=$(cat ./flags | awk -v n=$cur 'FNR == n')
if [[ $(echo $flag | grep -c "ssh") -eq 1 ]]; then
	ssh bandit$cur@bandit.labs.overthewire.org -i "$flag" -p 2220
else
	sshpass -p "$flag" ssh bandit$cur@bandit.labs.overthewire.org -p 2220
fi
