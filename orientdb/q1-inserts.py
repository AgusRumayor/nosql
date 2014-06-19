#!/usr/bin/python

import sys
import requests as r
import urllib

last_code = None
last_country = None
last_admin1 = None
last_admin2 = None
last_admin3 = None
cases = 0
cmdurl = "http://localhost:2480/command/exp/sql/"

req= r.post(cmdurl+"CREATE VERTEX World SET name ='Earth'", auth=('admin', 'admin'))
world = urllib.quote_plus(req.json()['result'][0]['@rid'])
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
    if admin3code == "":
	admin3code = admin3name

    country = urllib.quote_plus(country.replace("'", "\\'"))
    code = urllib.quote_plus(code.replace("'", "\\'"))
    place = urllib.quote_plus(place.replace("'", "\\'"))
    admin1name = urllib.quote_plus(admin1name.replace("'", "\\'"))
    admin2name = urllib.quote_plus(admin2name.replace("'", "\\'"))
    admin3name = urllib.quote_plus(admin3name.replace("'", "\\'"))

    req= r.post(cmdurl+"CREATE VERTEX Place SET name ='%s'" % place, auth=('admin', 'admin'))
    placen = urllib.quote_plus(req.json()['result'][0]['@rid'])
    if last_country != country:
	    req= r.post(cmdurl+"CREATE VERTEX Country SET name ='%s'" % country, auth=('admin', 'admin'))
	    cnode = urllib.quote_plus(req.json()['result'][0]['@rid'])
	    req= r.post(cmdurl+"CREATE EDGE Division FROM %s TO %s" % (world, cnode), auth=('admin', 'admin'))
	    last_country = country
    if cases > 1:
	if last_admin1 != admin1name:
	    req= r.post(cmdurl+"CREATE VERTEX Admin1 SET name ='%s'" % admin1name, auth=('admin', 'admin'))
	    a1 = urllib.quote_plus(req.json()['result'][0]['@rid'])
	    req= r.post(cmdurl+"CREATE EDGE Division FROM %s TO %s" % (cnode, a1), auth=('admin', 'admin'))
	    last_admin1 = admin1name
    if cases > 2:
	if last_admin2 != admin2name:
	    req= r.post(cmdurl+"CREATE VERTEX Admin2 SET name ='%s'" % admin2name, auth=('admin', 'admin'))
	    a2 = urllib.quote_plus(req.json()['result'][0]['@rid'])
	    req= r.post(cmdurl+"CREATE EDGE Division FROM %s TO %s" % (a1, a2), auth=('admin', 'admin'))
	    last_admin2 = admin2name
    if cases > 3:
	if last_admin3 != admin3name:
	    req= r.post(cmdurl+"CREATE VERTEX Admin3 SET name ='%s'" % admin3name, auth=('admin', 'admin'))
	    a3 = urllib.quote_plus(req.json()['result'][0]['@rid'])
	    req= r.post(cmdurl+"CREATE EDGE Division FROM %s TO %s" % (a2, a3), auth=('admin', 'admin'))
	    last_admin3 = admin3name
    if last_code != code:
	    req= r.post(cmdurl+"CREATE VERTEX Code SET name ='%s'" % code, auth=('admin', 'admin'))
	    coden = urllib.quote_plus(req.json()['result'][0]['@rid'])
	    last_code = code
	    if cases == 4:
		req= r.post(cmdurl+"CREATE EDGE Division FROM %s TO %s" % (a3, coden), auth=('admin', 'admin'))
	    if cases == 3:
		req= r.post(cmdurl+"CREATE EDGE Division FROM %s TO %s" % (a2, coden), auth=('admin', 'admin'))
	    if cases == 2:
		req= r.post(cmdurl+"CREATE EDGE Division FROM %s TO %s" % (a1, coden), auth=('admin', 'admin'))
	    if cases < 2:
		req= r.post(cmdurl+"CREATE EDGE Division FROM %s TO %s" % (cnode, coden), auth=('admin', 'admin'))

    req= r.post(cmdurl+"CREATE EDGE Division FROM %s TO %s" % (coden, placen), auth=('admin', 'admin'))

