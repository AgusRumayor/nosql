#!/usr/bin/python
from cassandra.cluster import Cluster

cluster = Cluster(['localhost'])
db = cluster.connect('exp')

#Get node by id
def q_node_id(identifier):
	tmp = db.execute('SELECT * FROM mexico WHERE id = %s', identifier)
	if (tmp== None):
		print "No se encuentra en la jerarquia id "+identifier
	else:
		print tmp

q_node_id(["CP01080"])
cluster.shutdown()
