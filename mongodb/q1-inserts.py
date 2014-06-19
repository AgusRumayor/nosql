#!/usr/bin/python

# Format of each line is:
# date\ttime\tstore name\titem description\tcost\tmethod of payment
#
# We want elements 2 (store name) and 4 (cost)
# We need to write them out to standard output, separated by a tab

import sys
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['exp']

world = db.mx

last_code = None
last_country = None
last_admin1 = None
last_admin2 = None
last_admin3 = None
cases = 0
earth = world.insert({"_id":"earth", "name":"Earth", "path":None})
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

    if last_country != country:
	    #new node country
	    country_node = world.insert({"_id":country, "name":country, "path":earth})
	    last_country = country
    if cases > 1:
	if last_admin1 != admin1name:
	    admin1_node = world.insert({"_id":admin1code, "name":admin1name, "path":earth+","+country_node})
	    last_admin1 = admin1name
    if cases > 2:
	if last_admin2 != admin2name:
	    admin2_node = world.insert({"_id":admin2code, "name":admin2name, "path":earth+","+country_node+","+admin1_node})
	    last_admin2 = admin2name
    if cases > 3:
	if last_admin3 != admin3name:
	    if admin3code != "":
	    	admin3_node = world.insert({"_id":admin2_node+","+admin3code, "name":admin3name, "path":earth+","+country_node+","+admin1_node+","+admin2_node})
	    else:
		admin3_node = world.insert({"_id":admin2_node+","+admin3name, "name":admin3name, "path":earth+","+country_node+","+admin1_node+","+admin2_node})
	    last_admin3 = admin3name
    if last_code != code:
	    if cases == 4:
		code_node = world.insert({"_id":"CP"+code, "name":code, "path":earth+","+country_node+","+admin1_node+","+admin3_node})
	    if cases == 3:
		code_node = world.insert({"_id":"CP"+code, "name":code, "path":earth+","+country_node+","+admin1_node+","+admin2_node})
	    if cases == 2:
		code_node = world.insert({"_id":"CP"+code, "name":code, "path":earth+","+country_node+","+admin1_node})
	    if cases < 2:
		code_node = world.insert({"_id":"CP"+code, "name":code, "path":earth+","+country_node})
	    last_code = code
    
    if cases == 4:
	place_node = world.insert({"name":place, "path":earth+","+country_node+","+admin1_node+","+admin3_node+","+code_node})
    if cases == 3:
	place_node = world.insert({"name":place, "path":earth+","+country_node+","+admin1_node+","+admin2_node+","+code_node})
    if cases == 2:
	place_node = world.insert({"name":place, "path":earth+","+country_node+","+admin1_node+","+code_node})
    if cases < 2:
	place_node = world.insert({"name":place, "path":earth+","+country_node+","+code_node})

#print "Total places added ",len(world)
	
