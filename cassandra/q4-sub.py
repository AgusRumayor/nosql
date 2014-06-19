#!/usr/bin/python
from cassandra.cluster import Cluster

cluster = Cluster(['localhost'])
db = cluster.connect('exp')

#Get subtree
def q_subtree(node):
	nodes = db.execute('SELECT * FROM mexico WHERE ancestors contains %s', node)
	for tmp in nodes:
		print tmp

q_subtree(["1001"])
cluster.shutdown()
