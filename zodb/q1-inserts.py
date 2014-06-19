#!/usr/bin/python

# Format of each line is:
# date\ttime\tstore name\titem description\tcost\tmethod of payment
#
# We want elements 2 (store name) and 4 (cost)
# We need to write them out to standard output, separated by a tab

import sys
import geoclasses
from treezodb import Tree
import ZODB, ZODB.FileStorage
import transaction

storage = ZODB.FileStorage.FileStorage('exp.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root
if hasattr(root, 'tree'):
	world = root.tree
else:
	root.tree = Tree()
	world = root.tree

last_code = None
last_country = None
last_admin1 = None
last_admin2 = None
last_admin3 = None
cases = 0
placecounter =0
earth = world.create_node("Earth", "earth")
for line in sys.stdin:
    data = line.strip().split("\t")
    if len(data) != 12:
	continue
    placecounter +=1
    country, code, place, admin1name, admin1code,admin2name, admin2code,admin3name, admin3code, lat, lon, accuracy = data
    if (admin1name != ""):
	cases=2
    	if (admin2name != ""):
	    cases=3
	    if (admin3name != ""):
		cases=4
    else:
	cases=1

    if admin3code == "":
	admin3code = admin3name
    if last_country != country:
	    #new node country
	    world.create_node(country, country, parent="earth")
	    last_country = country
    if cases > 1:
	if last_admin1 != admin1name:
	    world.create_node(admin1name, admin1code, parent=country)
	    if cases > 2:
	    	world.create_node(admin2name, admin2code, parent=admin1code)
	    if cases > 3:
	    	world.create_node(admin3name, admin3code, parent=admin2code)
	    last_admin1 = admin1name
	elif last_admin2 != admin2name:
	    if(world.get_node(admin2code)==None):
	    	world.create_node(admin2name, admin2code, parent=admin1code)
	    if(world.get_node(admin3code)==None) and cases > 2:
	    	world.create_node(admin3name, admin3code, parent=admin2code)
	    last_admin2 = admin2name
    	elif last_admin3 != admin3name:
	    if(world.get_node(admin3code)==None):
	    	world.create_node(admin3name, admin3code, parent=admin2code)
	    last_admin3 = admin3name
    if last_code != code:
	    if cases == 4:
		world.create_node(code, "CP"+code, parent=admin3code)
	    if cases == 3:
		world.create_node(code, "CP"+code, parent=admin2code)
	    if cases == 2:
		world.create_node(code, "CP"+code, parent=admin1code)
	    if cases < 2:
		world.create_node(code, "CP"+code, parent=country)
	    last_code = code

    world.create_node(place, "P"+str(placecounter), parent="CP"+code)
transaction.commit()
print "Total places added ",len(world)
	
