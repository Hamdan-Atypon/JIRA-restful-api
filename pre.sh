#!/bin/bash
export branch=$(echo $ATYPON_HOME | cut -d '/' -f5 | cut -d '-' -f2)
export host=$HOSTNAME
user='cip'
src='/local/home/ci/jenkins_agents/'${host}'_agent/workspace/'${branch}'/Unittest/test-results'
echo $user@$host:$src
#scp -r $user@$host:$src .
#
#grep 'failures="0'    -L ./test-results/* >> ./file
#grep 'error message=' -l ./test-results/* >> ./file
#cat ./file | sort | uniq  > ./file

echo "" > /tmp/file 
grep 'failures="0'    -L $src/* >> /tmp/file  
grep 'error message='  -l $src/* >> /tmp/file 
cd /tmp
cat ./file | grep -v 'TESTS-TestSuites.xml' | sort | uniq > ./.tmp
mkdir ./test_results
cat ./.tmp | xargs -i cp {} ./test_results/
cat ./.tmp | xargs -i basename -a {} >> ./source_list
sed -i 's/\.xml/\ /g' source_list
sed -i 's/TEST-com\.//g' source_list
