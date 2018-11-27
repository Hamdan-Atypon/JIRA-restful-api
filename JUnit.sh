#!/bin/bash
cd /tmp


while read line; do
  echo "$line"
  com=${line##*.}
  var=`python chk_issue.py -j ' text ~ "Broken Unit Test : '$com'" and status = Open '`
  if [ $var -gt 0 ]
  then
	echo "issue is already opened"  
  else
	echo "openning new issue .."
	tmp=`locate $com | grep HEAD  | grep '\.java'`
	dest=`grep '@report_to =' $tmp |  grep -o '[^ ]*@atypon.*' | awk -F"@" '{print $1}'`
	if [ -z $dest ]
	then
		echo "reporting to ops backlog"
		dest="hradaideh"
	else
		echo "reporting to "$dest
	fi
	file=`find test_results | grep $com`
        python write_jira.py -c $com -a $dest -b $BRANCH -f $file
  fi
  echo
done < source_list_$BRANCH
rm -rf .tmp_$BRANCH source_list_$BRANCH file_$BRANCH test_results_$BRANCH/
