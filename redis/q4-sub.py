#!/usr/bin/python

import redis

r= redis.StrictRedis(host='localhost', port=6379, db=9)

#Get subtree
def q_subtree(key):
	subtree = r.zrangebyscore('desc:'+key, '-inf', '+inf')
	print subtree

q_subtree("1001")
