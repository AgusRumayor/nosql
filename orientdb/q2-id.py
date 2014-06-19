#!/usr/bin/python
import sys
import requests as r
import urllib

cmdurl = "http://localhost:2480/command/mexico/sql/"

#Get node by id
def q_node_id(identifier):
	identifier = urllib.quote_plus(identifier.replace("'", "\\'"))
	req= r.post(cmdurl+"SELECT * FROM %s" % identifier, auth=('admin', 'admin'))
	print req.text

q_node_id("#14:5508")
