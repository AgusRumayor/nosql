#!/usr/bin/python

from treezodb import Tree
from node import Node

import ZODB, ZODB.FileStorage
import transaction

storage = ZODB.FileStorage.FileStorage('exp.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root
if hasattr(root, 'tree'):
	tree = root.tree
else:
	exit(0)

#Get node from id
def q_node_id(identifier):
	tmp = tree.get_node(identifier)
	if (tmp== None):
		print "No se encuentra en la jerarquia"
	else:
		print tmp.tag

q_node_id("CP01080")
