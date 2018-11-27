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
import getopt
username="opsbot"
password="bugz111a"
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
        res = requests.get("".join([jira_host,'rest/api/2/search?jql=',jql]), auth=HTTPBasicAuth(username,password))
        jsn = json.loads(res.text)
def select(num):
	global SELECTED
	SELECTED=num
def show(var):
	if SELECTED == -1:
	  print("please select a issue first")
	  return
	x=jsn["issues"][SELECTED]["fields"][var]
	print(json.dumps(x, indent=2))
def print_issues():
	global SELECTED
	global jsn
	print("Num	Summary")
	for x in range(0, jsn["total"]):
		print x,"	",jsn["issues"][x]["fields"]["summary"]
		
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

try:
    opts, args = getopt.getopt(sys.argv[1:], "hd:j:", ["help=", "debug=", "jql="])
except getopt.GetoptError as e:
    print e
    print "Error parsing arguments."
    sys.exit(2)
debug = None
for opt, arg in opts:
    if opt in ("-h", "--help"):
        print "chk_issue.py -h|--help -j|--jql -d|--debug\n\
                ex : python chk_issue.py -j ' text ~ \"Broken Unit Test : example.java\" and status = Open ' -d 1"
        sys.exit(1)
    elif opt in ("-j", "--jql"):
        jql = arg
    elif opt in ("-d", "--debug"):
        debug = arg

if jql == "":
    print "[-] No JQL to search .."
    exit()

init()
select(0)
if jsn["total"] > 0:
    print 1
else:
    print 0
if (debug == "1") and ( jsn["total"] > 0):
    print_issues()
    print_issue()
