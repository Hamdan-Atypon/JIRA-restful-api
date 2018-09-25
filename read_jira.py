#!/usr/bin/python
import requests
import json
import auth
from IPython import embed
from requests.auth import HTTPBasicAuth
import sys
import getpass
import os
from os import environ
#print os.environ[""]

username=""
password=""
jira_host="https://jira.atypon.com/"
jql=""
res=""
jsn=""

def help():
	print '''
select(num)		to select or reselect an issue, num indecates the issue number
print_issues()		print all issues
print_issue()		print all the data for specific issue
show(var)		print specific field, show("summary"), show("priority")
search(data, target)	search("Hamdan", "summary")

'''
def init():
	global SELECTED
        global username, password, jira_host, jql, res, jsn
	SELECTED=-1
        if environ.get('JIRA_UN') is not None:
            username=environ["JIRA_UN"]
        if username is "":
            username=raw_input('Enter your username\n')
        #else:
        #    print "using the global username"
        if environ.get('JIRA_PW') is not None:
            password=environ["JIRA_PW"]
        if password is "":
            password=getpass.getpass()
        else:
            print "using the global username and password ..."
        print "using the Jira host : ",jira_host
        print ""
        jql=raw_input('Enter your jql query [summary~\"Al-Radaideh\"]\n')
        if jql is "":
            jql="summary~\"Al-Radaideh\"";
        
        print "wait until finish pulling the data .."
        res = requests.get("".join([jira_host,'rest/api/2/search?jql=',jql]), auth=HTTPBasicAuth(username,password))
        #print(res)
        jsn = json.loads(res.text)
def select(num):
	global SELECTED
	SELECTED=num
	print(SELECTED)
def show(var):
	if SELECTED == -1:
	  print("please select a issue first")
	  return
	x=jsn["issues"][SELECTED]["fields"][var]
	print(json.dumps(x, indent=2))
def print_issues():
	global SELECTED
	#print(SELECTED)
	global jsn
	print("Num	Summary")
	for x in range(0, jsn["total"]):
		print x,"	",jsn["issues"][x]["fields"]["summary"]
def search(data, target):
	global jsn
	list1 = ["summary", "created", "desciption"]
	list2 = ["assignee", "creator", "reporter"]
	list3 = ["priority", "project", "status"]
        for x in range(0, jsn["total"]):
		if target in list1:
			if data in jsn["issues"][x]["fields"][target]:
                		print x,"       ",jsn["issues"][x]["fields"][target]
		if target in list2:
			if data in jsn["issues"][x]["fields"][target]["displayName"]:
                		print x,"       ",jsn["issues"][x]["fields"][target]["displayName"]
		if target in list3:
			if data in jsn["issues"][x]["fields"][target]["name"]:
                		print x,"       ",jsn["issues"][x]["fields"][target]["name"]
		if target is "Ticket_ID":
			print x,"	",jsn["issues"][x]["key"]
		
def print_issue():
	id=SELECTED
	print "Ticket_ID   :","\t\t", 	jsn["issues"][id]["key"]
	print "Assignee    :","\t\t", 	jsn["issues"][id]["fields"]["assignee"]["displayName"]
	print "Summary     :","\t\t", 	jsn["issues"][id]["fields"]["summary"]
	print "Creator     :","\t\t", 	jsn["issues"][id]["fields"]["creator"]["displayName"]
        print "Reporter    :","\t\t", 	jsn["issues"][id]["fields"]["reporter"]["displayName"]
        print "Created     :","\t\t", 	jsn["issues"][id]["fields"]["created"]
        print "Priority    :","\t\t", 	jsn["issues"][id]["fields"]["priority"]["name"]
	print "Project     :","\t\t", 	jsn["issues"][id]["fields"]["project"]["name"]
        print "Status      :","\t\t",	jsn["issues"][id]["fields"]["status"]["name"]
        print "Description :","\t\t\n",	jsn["issues"][id]["fields"]["description"]
init()
os.system('clear')
print_issues()
print ""
embed()

