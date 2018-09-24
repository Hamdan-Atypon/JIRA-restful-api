#!/bin/python

from jira import JIRA
import webbrowser
import json
from os import environ
import getpass
import getopt
import sys

username=""
password=""
jira_host="https://jira.atypon.com/"

def init():
        global username, password
        if environ.get('JIRA_UN') is not None:
            username=environ["JIRA_UN"]
        if username is "":
            username=raw_input('Enter your username\n')
        if environ.get('JIRA_PW') is not None:
            password=environ["JIRA_PW"]
        if password is "":
            password=getpass.getpass()
        else:
            print "using the global username and password ..."
        print "using the Jira host : ",jira_host

versions_map = dict()
versions_map.update({"trunk": "10043"})
versions_map.update({"1820": "15142"})
versions_map.update({"1810": "14416"})
versions_map.update({"1730": "13468"})
versions_map.update({"1720": "13467"})
versions_map.update({"1710": "13207"})
versions_map.update({"1630": "12701"})
versions_map.update({"1620": "12401"})
versions_map.update({"1610": "11904"})
versions_map.update({"1530": "10703"})
versions_map.update({"1520": "10702"})
versions_map.update({"1510": "10303"})


try:
    opts, args = getopt.getopt(sys.argv[1:], "hf:c:a:b:d:i:", ["help=", "file=", "component=", "assignee=",
                                                                 "branches="])
except getopt.GetoptError as e:
    print "Error parsing arguments."
    sys.exit(2)
attachment_name = None
component = None
assignee = None
branches = None
for opt, arg in opts:
    if opt in ("-h", "--help"):
        print "python write_jira.py -c|--component -a|--assignee -b|--branches (comma separated)" \
              " -f| attatchment"
        sys.exit(1)
    elif opt in ("-c", "--component"):
        component = arg
    elif opt in ("-a", "--assignee"):
        assignee = arg
    elif opt in ("-b", "--branches"):
        branches = arg
    elif opt in ("-f", "--file"):
        attachment_name = arg

if ( component == None ) or ( assignee == None ) or ( branches == None ):
    print "not all arguments is entered, Exiting .."
    exit()
init()
jira = JIRA(server=jira_host, basic_auth=( username, password ))

labels = ["UNIT-TESTS"]
#the_component="example.java"
#the_assignee="hradaideh"
#branches="1820"
the_component=component
the_assignee=assignee
branches=branches
description = "Hi,\r\n\r\n{} has or causes broken tests.  Can you please have a look?\r\n\r\n\r\n\r\nThanks!". \
            format(the_component)
summary = "Broken Unit Test : {}".format(the_component)
priority = "P3 (Normal)"
severity = "P3"


versions = list()

for branch in branches.split(","):
    versions.append({"id": versions_map[branch]})

issue_dict = {
    'project': {"key": "LIT"},
    'issuetype': {"name": "Bug"},
    'components': [{"name": "LIT-BTD"}],
    'assignee': {"name": the_assignee},
    'description': description,
    'summary': summary,
    'customfield_10500': [{"value": "Multi"}],
    'versions': versions,
    'labels': labels,
    'customfield_10500': None,
    'priority': { "name" : priority }
}

print(json.dumps(issue_dict, indent=4))
print "please wait while creating the issue and uploading the file .."
issue = jira.create_issue(fields=issue_dict)
attachment_name="example.java"

if attachment_name is not None:
    with open("/home/hradaideh/" + attachment_name, 'rb') as the_attachment:
        jira.add_attachment(issue, the_attachment, attachment_name)
print ""
print "issue created with ID: ",issue
print ""
#webbrowser.open_new("https://jira.atypon.com/browse/{}".format(issue))
