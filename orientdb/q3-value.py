#!/usr/bin/python
import sys
import requests as r
import urllib

cmdurl = "http://localhost:2480/command/mexico/sql/"

#Get node by value
def q_nodes_value(value):
	value = urllib.quote_plus(value.replace("'", "\\'"))
	req= r.post(cmdurl+"SELECT * FROM V WHERE name = '%s'" % value, auth=('admin', 'admin'))
	print req.text

q_nodes_value("Aguascalientes")
