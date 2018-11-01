from node import Node

class Tree(object):
	def __init__(self, rootNode):
		self.root = rootNode

	def predict_proba(self, x):
		"""
		x : one row of features
		"""
		node = self.root
		while node.isLeaf is False:
			v, split = node.varIndex, node.splitValue
			if x[v] > split:
				node = node.right
			else:
				node = node.left
		return node.classProb

	def draw(self):
		"""
		pre-order traversal of tree
		"""
		self._print(self.root, 0)

	def _print(self, node, i):
		if node is not None:
			if node.isLeaf:
				print "N/A", "N/A", "N/A", node.classProb
			else:
				print node.varIndex, node.splitValue, node.infogain, node.classProb
			i = self._print(node.left, i)
			i = self._print(node.right, i)