from node import Node
from tree import Tree
import numpy as np

class TreeBuilder(object):
	def __init__(self, X, y, min_leaf_samples=10):
		self.X = np.array(X)
		self.y = np.array(y)
		self.min_leaf_samples = min_leaf_samples
		self.tree = self._build()

	def _build(self):
		p = self.y.sum()/(1.0 * self.y.shape[0])
		if p != 0 and p!= 1:
			root, root_leftIndices, root_rightIndices = self._best_split(np.arange(self.X.shape[0]))
			tree = Tree(root)
			self._build_node(root, root_leftIndices, root_rightIndices)
			return tree
		else:
			print "Warning ! All instances belong to the same class"

	def _build_node(self, parentNode, leftIndices, rightIndices):

		pLeft = self.y[leftIndices].sum()/(1.0 * leftIndices.shape[0])
		pRight = self.y[rightIndices].sum()/(1.0 * rightIndices.shape[0])
		if leftIndices.size >= self.min_leaf_samples and pLeft > 0.0 and pLeft < 1.0:
			left_node, left_leftIndices, left_rightIndices = self._best_split(leftIndices)
			parentNode.left = left_node
			self._build_node(left_node, left_leftIndices, left_rightIndices)
		else:
			left_node = Node(classProb=pLeft, isLeaf=True)
			parentNode.left = left_node

		if rightIndices.size >= self.min_leaf_samples and pRight > 0.0 and pRight < 1.0:
			right_node, right_leftIndices, right_rightIndices = self._best_split(rightIndices)
			parentNode.right = right_node
			self._build_node(right_node, right_leftIndices, right_rightIndices)
		else:
			right_node = Node(classProb=pRight, isLeaf=True)
			parentNode.right = right_node

	def _best_split(self, indices, parentEntropy=None):
		"""
		compute the best variable to split on based on information gain and also return the left and right indices
		"""
		best_var = None
		best_splitval = None
		best_leftIndices = None
		best_rightIndices = None
		best_ig = -1

		if parentEntropy is None:
			parentEntropy = self._entropy(indices)

		for i in range(self.X.shape[1]):
			# iterate over the unique values of column i
			x_uniq = sorted(list(set(self.X[indices, i])))
			if len(x_uniq) == 1:
				continue
			for x in x_uniq[:-1]:
				leftIndices = indices[self.X[indices, i] <= x]
				rightIndices = indices[self.X[indices, i] > x]
				info_gain = self._information_gain(parentEntropy, indices, leftIndices, rightIndices)
				if info_gain > best_ig:
					best_ig = info_gain
					best_leftIndices = leftIndices
					best_rightIndices = rightIndices
					best_var = i
					best_splitval = x
		node = Node(varIndex=best_var, splitValue=best_splitval, infogain=best_ig)
		return node, best_leftIndices, best_rightIndices


	def _information_gain(self, parentEntropy, parentIndices, leftIndices, rightIndices):
		"""
		return the information gain 
		"""
		# parentEntropy = self._entropy(parentIndices)
		leftEntropy = self._entropy(leftIndices)
		rightEntropy = self._entropy(rightIndices)
		pL = leftIndices.shape[0]/(1.0 * parentIndices.shape[0])
		pR = 1 - pL
		ig = parentEntropy - (pL * leftEntropy + pR * rightEntropy)
		return ig

	def _entropy(self, indices):
		"""
		return the entropy value of the distribution of labels
		"""
		p1 = self.y[indices].sum()/(1.0 * indices.shape[0])
		p0 = 1 - p1
		if p0 == 1 or p1 == 1:
			return 0
		return -(p0 * np.log2(p0) + p1 * np.log2(p1))