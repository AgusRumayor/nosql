#!/usr/bin/python
from cassandra.cluster import Cluster

cluster = Cluster(['localhost'])
db = cluster.connect('exp')

#Get node by value
def q_nodes_value(value):
	nodes = db.execute('SELECT * FROM mexico WHERE name = %s ALLOW FILTERING', value)
	for tmp in nodes:
		print tmp

q_nodes_value(["Aguascalientes"])
cluster.shutdown()
