#!/usr/bin/python
from py2neo import node, rel, neo4j
graph = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

#Get subtree
def q_subtree(node):
	query = neo4j.CypherQuery(graph, "start n=node(%s) match n-[r*]->m return distinct m;" % node)
	for record in query.stream():
		info = unicode(record[0])
		print info.encode('utf-8')

q_subtree("847")
