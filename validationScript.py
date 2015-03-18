
from validation import *

v = validation()
v.loadSimDict()

N = len(v.nodes)

# benchmark
v.random = True
v.correctPred(K1 = N-1)
bench = v.correctlyPredicted

# varying K
v.random = False
correctTies = []
for i in xrange(1,N-1):
	print i
	v.correctPred(K1 = i)
	correctTies += [v.correctlyPredicted]