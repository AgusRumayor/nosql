#!/usr/bin/python

from py2neo import node, rel, neo4j

graph = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

#Get node by id
def q_node_id(identifier):
	query = neo4j.CypherQuery(graph, "START n=node(%s) return n" % identifier)
	for record in query.stream():
		info = unicode(record[0])
		print info.encode('utf-8')

q_node_id("20937")
