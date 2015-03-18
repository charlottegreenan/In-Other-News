#!/usr/bin/python -tt

from initialize import *

class findNearestNeighbors(initialize):
	def __init__(self):
		initialize.__init__(self)
		self.egoToRemove = 0
		self.K1 = 125
		self.knownSimDict = False
		self.simDict = {}
	
	## Return K1 most similar nodes, along with their similarity.
	## If knownSimDict = True, then list1 is the node, not the list of sections (this
	## is to speed up calculations when doing validation).
	def similarNodes(self, list1):
		self.topChoices = []
		a = []
		for id2 in self.nodes:
			if id2 != self.egoToRemove:
				sim2 = 0
				if self.knownSimDict:
					if (list1,id2) in self.simDict:
						sim1 = self.simDict[(list1,id2)]
					else:
						sim1 = 0.0
				else:
					sim1 = self.cosSim(list1, id2)
				a += [(sim1,id2)]
		self.topChoices = sorted(a, reverse=True)[:self.K1]
