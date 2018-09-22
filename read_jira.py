import requests
import json
import auth
from IPython import embed
from requests.auth import HTTPBasicAuth
import sys
import getpass

username=raw_input('Enter your username\n')
password=getpass.getpass()
print "ex:" , "summary~\"Al-Radaideh\""
jbl=raw_input('Enter your jbl query\n')

res = requests.get("".join(['https://jira.atypon.com/rest/api/2/search?jql=',jbl]), auth=HTTPBasicAuth(username,password))
print(res)
jsn = json.loads(res.text)

def help():
	print '''
select(num)		to select or reselect an issue, num indecates the issue number
print_issues()		print all issues
show(var)		print specific field, show("summary"), show("priority")
search(data, target)	search("Hamdan", "summary")
'''
def init():
	global SELECTED
	SELECTED=-1
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
	print(SELECTED)
	global jsn
	print("Num	Summary")
	for x in range(0, jsn["total"]):
		print x,"	",jsn["issues"][x]["fields"]["summary"]
def search(data, target):
	global jsn
        for x in range(0, jsn["total"]):
		if data in jsn["issues"][x]["fields"][target]:
                	print x,"       ",jsn["issues"][x]["fields"]["summary"]
init()
print_issues()
embed()

