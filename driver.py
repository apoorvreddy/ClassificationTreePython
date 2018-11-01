from tree_builder import TreeBuilder
import pandas as pd
import numpy as np

X = [
	[2,5,6,1],
	[1,5,4,1],
	[2,5,5,2],
	[3,15,6,5],
	[3,10,6,3],
	[2,10,6,4],
	[2,15,5,5],
	[1,10,4,1],
	[3,5,5,3],
	[3,15,4,2],
	[1,15,4,1],
	[3,10,4,4]]

y = [1]*5 + [0]*7

tree = TreeBuilder(X, y, 2)
tree.tree.draw()