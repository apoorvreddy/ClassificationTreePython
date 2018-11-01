class Node(object):
	def __init__(self, varIndex=None, splitValue=None, infogain=None, classProb=None, isLeaf=False):
		self.left = None
		self.right = None
		self.infogain = infogain
		self.isLeaf = isLeaf
		self.varIndex = varIndex
		self.splitValue = splitValue
		self.classProb = classProb