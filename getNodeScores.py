#!/usr/bin/python -tt

from findNearestNeighbors import *

class getNodeScores(findNearestNeighbors):
	def __init__(self):
		findNearestNeighbors.__init__(self)
		self.lambda1 = 0.5
		self.returnTieStrength = True
		self.random = False
	
	def getScores(self, list):
		self.similarNodes(list)
		self.scores = {}
		self.scoresFromUpvotes()
		self.scoresFromNearestNeighbours()

	## Adds specified weight to scores for all alters of nodes
	def addToScores(self, node, weight):
		if self.friendsList[node]:
			for alter1 in self.friendsList[node]:
				if alter1 in self.scores:
					self.scores[alter1] += weight
				else:
					self.scores[alter1] = weight

	## Adds contributions to scores for the alters of upvoted nodes myties
	def scoresFromUpvotes(self):
		if self.myties:
			rat2 = (1-self.lambda1)/float(len(self.myties))
			for tie in self.myties:
				self.addToScores(tie, rat2)

	## Adds contributions to scores for the alters of similar nodes topChoices
	def scoresFromNearestNeighbours(self):
		if self.topChoices:
			if self.random:
				sum1 = len(self.topChoices)
			else:
				sum1 = sum([c[0] for c in self.topChoices])
			if not sum1:
				sum1 = 1
		for node in self.topChoices:
			if self.random:
				rat1 = 1.0/sum1
			else:
				rat1 = node[0]/sum1
			self.addToScores(node[1], self.lambda1*rat1)
