#!/usr/bin/python
import sys
import requests as r
import urllib

cmdurl = "http://localhost:2480/command/mexico/sql/"

#Get subtree
def q_subtree(node):
	node = urllib.quote_plus(node.replace("'", "\\'"))
	req= r.post(cmdurl+"TRAVERSE out_Division FROM %s" % node, auth=('admin', 'admin'))
	print req.text

q_subtree("#12:0")
