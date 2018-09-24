# JIRA-restful-api

This project made to pull data from Jira using it's API and write new issues,
You can set your password as username and password in the current shell using the following command

	. ./set_env.sh

then install the python requirments using this as root

	pip install -r requirements.txt

to run the script for pulling the Data use this
	
	python read_jira.py

to write a new issue, check this

	python write_jira.py -h

check for specific JQL, returns 1 if there is one or more matches, for usage check this

	python chk_issue.py -h
