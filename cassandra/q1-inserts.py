#!/usr/bin/python

# Format of each line is:
# country, code, place, admin1name, admin1code,admin2name, admin2code,admin3name, admin3code, lat, lon, accuracy
#
# 
# separated by a tab

import sys
from cassandra.cluster import Cluster

cluster = Cluster(['localhost'])
db = cluster.connect('exp')

last_code = None
last_country = None
last_admin1 = None
last_admin2 = None
last_admin3 = None
placecounter = 0
cases = 0
db.execute("INSERT INTO mexico (id, name, ancestors, tags) VALUES (%(id)s, %(name)s, %(path)s, %(tag)s )",{"id":"earth", "name":"Earth", "path":None, "tag":['World']})
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

    ancestors = ['earth']
    if last_country != country:
	    #new node country
	    db.execute("INSERT INTO mexico (id, name, ancestors, tags) VALUES (%(id)s, %(name)s, %(path)s, %(tag)s )",{"id":country, "name":country, "path":ancestors, "tag":['Country']})
	    last_country = country
    ancestors.append(country)
    if cases > 1:
	if last_admin1 != admin1name:
	    db.execute("INSERT INTO mexico (id, name, ancestors, tags) VALUES (%(id)s, %(name)s, %(path)s, %(tag)s )",{"id":admin1code, "name":admin1name, "path":ancestors, "tag":['Admin1']})
	    last_admin1 = admin1name
    ancestors.append(admin1code)
    if cases > 2:
	if last_admin2 != admin2name:
	    db.execute("INSERT INTO mexico (id, name, ancestors, tags) VALUES (%(id)s, %(name)s, %(path)s, %(tag)s )",{"id":admin2code, "name":admin2name, "path":ancestors, "tag":['Admin2']})
	    last_admin2 = admin2name
    ancestors.append(admin2code)
    if cases > 3:
	if last_admin3 != admin3name:
	    db.execute("INSERT INTO mexico (id, name, ancestors, tags) VALUES (%(id)s, %(name)s, %(path)s, %(tag)s )",{"id":admin2code+"/"+admin3code, "name":admin3name, "path":ancestors, "tag":['Admin3']})
	    last_admin3 = admin3name
    ancestors.append(admin3code)
    if last_code != code:
	    db.execute("INSERT INTO mexico (id, name, ancestors, tags) VALUES (%(id)s, %(name)s, %(path)s, %(tag)s )",{"id":"CP"+code, "name":code, "path":ancestors, "tag":['Code']})
	    last_code = code
    ancestors.append("CP"+code)
    db.execute("INSERT INTO mexico (id, name, ancestors, tags) VALUES (%(id)s, %(name)s, %(path)s, %(tag)s )",{"id":"P"+str(placecounter), "name":place, "path":ancestors, "tag":['Place']})

#print "Total places added ",len(world)
cluster.shutdown()
