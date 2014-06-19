#!/usr/bin/python

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['exp']

world = db.mx

#Get node by value
def q_nodes_value(value):
	nodes = world.find({"name":value})
	for tmp in nodes:
		print tmp

q_nodes_value("Aguascalientes")
