#!/usr/bin/python

import redis

r= redis.StrictRedis(host='localhost', port=6379, db=8)

#Get node by id
def q_node_id(key):
	node = r.get(key)
	if node != None:
		print node

q_node_id("CP01080")
