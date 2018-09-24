#!/bin/bash

while read line; do
  echo "$line"
  var=`python ./chk_issue.py -j ' text ~ "Broken Unit Test : '$line'" and status = Open '`
  if [ $var -gt 0 ]
  then
	echo "issue is already opened"  
  else
	echo "openning new issue .."
	file=`find /home/hradaideh/JIRA-restful-api | grep ${line::-4}`
	dest=`grep '@report_to =' $file |  grep -o '[^ ]*@atypon.*' | awk -F"@" '{print $1}'`
	if [ -z $dest ]
	then
		echo "reporting to ops backlog"
		exe=`python write_jira.py -c $line -a ops   -b 1820 -f /home/hradaideh/JIRA-restful-api/$line`
		echo $exe
	else
		echo "reporting to "$dest
                exe=`python write_jira.py -c $line -a $dest -b 1820 -f /home/hradaideh/JIRA-restful-api/$line`
		echo $exe

	fi

  fi
  echo
done < file
