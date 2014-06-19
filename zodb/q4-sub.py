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

#Get subtree
def q_subtree(identifier):
	tmp = tree.subtree(identifier)
	tmp.show()

q_subtree("1001")
