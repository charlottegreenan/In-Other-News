#!/usr/bin/python -tt

from getNodeScores import *

class chooseTies(getNodeScores):
	def run(self, list): 
		self.getScores(list)
		orderedAlters = sorted(self.scores.items(), reverse=True, key=self.mykey2)
		self.alters = []
		### add myties to alters
		self.recSec = set([])
		self.sectionsWithRecommendations(self.alters)
		
		## Adding nodes to alters until we have recommended as many sections as
		## possible.
		j = 0
		nRec = 8
		while len(self.recSec) < nRec and j < len(orderedAlters):
			if sum([sect not in self.recSec for sect in self.sections[orderedAlters[j][0]]]) > 0:
				if orderedAlters[j][0] not in self.excludedNodes:
					if self.returnTieStrength:
						self.alters += [orderedAlters[j]]
					else:
						self.alters += [orderedAlters[j][0]]
					self.sectionsWithRecommendations([self.alters[-1]])
			j+=1

	def sectionsWithRecommendations(self, alters):
		if alters:
			for alter in alters:
				if self.returnTieStrength:
					a = alter[0]
				else:
					a = alter
				self.recSec = self.recSec.union(set(self.sections[a]))








