#!/usr/bin/python

# Format of each line is:
# date\ttime\tstore name\titem description\tcost\tmethod of payment
#
# We want elements 2 (store name) and 4 (cost)
# We need to write them out to standard output, separated by a tab

import sys
from py2neo import node, rel, neo4j

graph = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
last_code = None
last_country = None
last_admin1 = None
last_admin2 = None
last_admin3 = None
cases = 0
graph.clear()
world, = graph.create(node({"name":"earth"}))
world.add_labels("world")
for line in sys.stdin:
    data = line.strip().split("\t")
    if len(data) != 12:
	continue
    country, code, place, admin1name, admin1code,admin2name, admin2code,admin3name, admin3code, lat, lon, accuracy = data
    if (admin1name != ""):
	cases=2
    	if (admin2name != ""):
	    cases=3
	    if (admin3name != ""):
		cases=4
    else:
	cases=1
    placen, = graph.create(node({"name":place}))
    placen.add_labels("place")
    if last_country != country:
	    cnode, = graph.create(node({"name":country}))
	    cnode.add_labels("country")
	    relation, = graph.create(rel(world, "division", cnode))
	    last_country = country
    if cases > 1:
	if last_admin1 != admin1name:
	    a1, = graph.create(node({"name":admin1name}))
	    a1.add_labels("admin1")
	    relation, = graph.create(rel(cnode, "division", a1))
	    last_admin1 = admin1name
    if cases > 2:
	if last_admin2 != admin2name:
	    a2, = graph.create(node({"name":admin2name}))
	    a2.add_labels("admin2")
	    relation, = graph.create(rel(a1, "division", a2))
	    last_admin2 = admin2name
    if cases > 3:
	if last_admin3 != admin3name:
	    a3, = graph.create(node({"name":admin3name}))
	    a3.add_labels("admin3")
	    relation, = graph.create(rel(a2, "division", a3))
	    last_admin3 = admin3name
    if last_code != code:
	    coden, = graph.create(node({"code":code}))
	    coden.add_labels("code")
	    last_code = code
	    if cases == 4:
		relation, = graph.create(rel(a3, "division", coden))
	    if cases == 3:
		relation, = graph.create(rel(a2, "division", coden))
	    if cases == 2:
		relation, = graph.create(rel(a1, "division", coden))
	    if cases < 2:
		relation, = graph.create(rel(cnode, "division", coden))

    #relations
    relation, = graph.create(rel(coden, "division", placen))
	
