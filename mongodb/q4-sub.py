#!/usr/bin/python

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['exp']

world = db.mx

#Get subtree
def q_subtree(node):
	nodes = world.find({"path":{"$regex":","+node}})
	for tmp in nodes:
		print tmp

q_subtree("1001")
