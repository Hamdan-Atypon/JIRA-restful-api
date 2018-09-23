#!/bin/bash

echo 
echo "This script sets the Username and Password as env variables"
echo "run it like this -> . ./set_env.sh"
echo

echo -n username:
read JIRA_UN
echo
echo -n Password: 
read -s JIRA_PW
echo
export JIRA_UN
export JIRA_PW

