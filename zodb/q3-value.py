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

#Get node by value
def q_nodes_value(tag):
	nodes = tree.search_tag(tag)
	for tmp in nodes:
		print tmp.identifier

q_nodes_value("Aguascalientes")
