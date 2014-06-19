#!/usr/bin/python

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['exp']

world = db.mx

#Get node by id
def q_node_id(identifier):
	tmp = world.find_one({"_id":identifier})
	if (tmp== None):
		print "No se encuentra en la jerarquia id "+identifier
	else:
		print tmp

q_node_id("CP01080")
