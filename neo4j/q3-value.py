#!/usr/bin/python

from py2neo import node, rel, neo4j

graph = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

#Get node by value
def q_nodes_value(value):
	query = neo4j.CypherQuery(graph, "MATCH (n) WHERE n.name='%s' RETURN n LIMIT 100" % value)
	for record in query.stream():
		info = unicode(record[0])
		print info.encode('utf-8')

q_nodes_value("Aguascalientes")
