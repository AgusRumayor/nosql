#!/usr/bin/python

# Format of each line is:
# country, code, place, admin1name, admin1code,admin2name, admin2code,admin3name, admin3code, lat, lon, accuracy
#
# 
# separated by a tab

import sys
import redis

r= redis.StrictRedis(host='localhost', port=6379, db=8)
rrel= redis.StrictRedis(host='localhost', port=6379, db=9)
r.flushdb()
rrel.flushdb()

last_code = None
last_country = None
last_admin1 = None
last_admin2 = None
last_admin3 = None
placecounter = 0
cases = 0
r.set('earth', 'Earth')
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
	    r.set(country, country)
	    rrel.zadd('desc:'+'earth', 1, country)
	    rrel.zadd('asc:'+country, 1, 'earth')
	    last_country = country
    if cases > 1:
	if last_admin1 != admin1name:
	    r.set(admin1code, admin1name)
	    rrel.zadd('desc:'+'earth', 2, admin1code)
	    rrel.zadd('desc:'+country, 1, admin1code)
	    rrel.zadd('asc:'+admin1code, 2, 'earth')
	    rrel.zadd('asc:'+admin1code, 1, country)
	    last_admin1 = admin1name
    if cases > 2:
	if last_admin2 != admin2name:
	    r.set(admin2code, admin2name)
	    rrel.zadd('desc:'+'earth', 3, admin2code)
	    rrel.zadd('desc:'+country, 2, admin2code)
	    rrel.zadd('desc:'+admin1code, 1, admin2code)
	    rrel.zadd('asc:'+admin2code, 3, 'earth')
	    rrel.zadd('asc:'+admin2code, 2, country)
	    rrel.zadd('asc:'+admin2code, 1, admin1code)
	    last_admin2 = admin2name
    if cases > 3:
	if last_admin3 != admin3name:
	    r.set(admin3code, admin3name)
	    rrel.zadd('desc:'+'earth', 4, admin3code)
	    rrel.zadd('desc:'+country, 3, admin3code)
	    rrel.zadd('desc:'+admin1code, 2, admin3code)
	    rrel.zadd('desc:'+admin2code, 1, admin3code)
	    rrel.zadd('asc:'+admin3code, 4, 'earth')
	    rrel.zadd('asc:'+admin3code, 3, country)
	    rrel.zadd('asc:'+admin3code, 2, admin1code)
	    rrel.zadd('asc:'+admin3code, 1, admin2code)
	    last_admin3 = admin3name
    if last_code != code:
	    if cases == 4:
		r.set("CP"+code, code)
	        rrel.zadd('desc:'+'earth', 5, "CP"+code)
	        rrel.zadd('desc:'+country, 4, "CP"+code)
	        rrel.zadd('desc:'+admin1code, 3, "CP"+code)
	        rrel.zadd('desc:'+admin2code, 2, "CP"+code)
		rrel.zadd('desc:'+admin3code, 1, "CP"+code)
	    	rrel.zadd('asc:'+"CP"+code, 5, 'earth')
	    	rrel.zadd('asc:'+"CP"+code, 4, country)
	    	rrel.zadd('asc:'+"CP"+code, 3, admin1code)
	    	rrel.zadd('asc:'+"CP"+code, 2, admin2code)
		rrel.zadd('asc:'+"CP"+code, 1, admin3code)
	    if cases == 3:
		r.set("CP"+code, code)
	        rrel.zadd('desc:'+'earth', 4, "CP"+code)
	        rrel.zadd('desc:'+country, 3, "CP"+code)
	        rrel.zadd('desc:'+admin1code, 2, "CP"+code)
	        rrel.zadd('desc:'+admin2code, 1, "CP"+code)
	    	rrel.zadd('asc:'+"CP"+code, 4, 'earth')
	    	rrel.zadd('asc:'+"CP"+code, 3, country)
	    	rrel.zadd('asc:'+"CP"+code, 2, admin1code)
	    	rrel.zadd('asc:'+"CP"+code, 1, admin2code)
	    if cases == 2:
		r.set("CP"+code, code)
	        rrel.zadd('desc:'+'earth', 3, "CP"+code)
	        rrel.zadd('desc:'+country, 2, "CP"+code)
	        rrel.zadd('desc:'+admin1code, 1, "CP"+code)
	    	rrel.zadd('asc:'+"CP"+code, 3, 'earth')
	    	rrel.zadd('asc:'+"CP"+code, 2, country)
	    	rrel.zadd('asc:'+"CP"+code, 1, admin1code)
	    if cases < 2:
		r.set("CP"+code, code)
	        rrel.zadd('desc:'+'earth', 2, "CP"+code)
	        rrel.zadd('desc:'+country, 1, "CP"+code)
	    	rrel.zadd('asc:'+"CP"+code, 2, 'earth')
	    	rrel.zadd('asc:'+"CP"+code, 1, country)
	    last_code = code
    
    r.set("P"+str(placecounter), place)
    if cases == 4:
        rrel.zadd('desc:'+'earth', 6, "P"+str(placecounter))
        rrel.zadd('desc:'+country, 5, "P"+str(placecounter))
        rrel.zadd('desc:'+admin1code, 4, "P"+str(placecounter))
        rrel.zadd('desc:'+admin2code, 3, "P"+str(placecounter))
	rrel.zadd('desc:'+admin3code, 2, "P"+str(placecounter))
	rrel.zadd('desc:'+"CP"+code, 1, "P"+str(placecounter))
    	rrel.zadd('asc:'+"P"+str(placecounter), 6, 'earth')
    	rrel.zadd('asc:'+"P"+str(placecounter), 5, country)
    	rrel.zadd('asc:'+"P"+str(placecounter), 4, admin1code)
    	rrel.zadd('asc:'+"P"+str(placecounter), 3, admin2code)
	rrel.zadd('asc:'+"P"+str(placecounter), 2, admin3code)
	rrel.zadd('asc:'+"P"+str(placecounter), 1, "CP"+code)
    if cases == 3:
	rrel.zadd('desc:'+'earth', 5, "P"+str(placecounter))
        rrel.zadd('desc:'+country, 4, "P"+str(placecounter))
        rrel.zadd('desc:'+admin1code, 3, "P"+str(placecounter))
        rrel.zadd('desc:'+admin2code, 2, "P"+str(placecounter))
	rrel.zadd('desc:'+"CP"+code, 1, "P"+str(placecounter))
    	rrel.zadd('asc:'+"P"+str(placecounter), 5, 'earth')
    	rrel.zadd('asc:'+"P"+str(placecounter), 4, country)
    	rrel.zadd('asc:'+"P"+str(placecounter), 3, admin1code)
    	rrel.zadd('asc:'+"P"+str(placecounter), 2, admin2code)
	rrel.zadd('asc:'+"P"+str(placecounter), 1, "CP"+code)
    if cases == 2:
	rrel.zadd('desc:'+'earth', 4, "P"+str(placecounter))
        rrel.zadd('desc:'+country, 3, "P"+str(placecounter))
        rrel.zadd('desc:'+admin1code, 2, "P"+str(placecounter))
	rrel.zadd('desc:'+"CP"+code, 1, "P"+str(placecounter))
    	rrel.zadd('asc:'+"P"+str(placecounter), 4, 'earth')
    	rrel.zadd('asc:'+"P"+str(placecounter), 3, country)
    	rrel.zadd('asc:'+"P"+str(placecounter), 2, admin1code)
	rrel.zadd('asc:'+"P"+str(placecounter), 1, "CP"+code)
    if cases < 2:
	rrel.zadd('desc:'+'earth', 3, "P"+str(placecounter))
        rrel.zadd('desc:'+country, 2, "P"+str(placecounter))
	rrel.zadd('desc:'+"CP"+code, 1, "P"+str(placecounter))
    	rrel.zadd('asc:'+"P"+str(placecounter), 3, 'earth')
    	rrel.zadd('asc:'+"P"+str(placecounter), 2, country)
	rrel.zadd('asc:'+"P"+str(placecounter), 1, "CP"+code)

#print "Total places added ",len(world)
	
