
from chooseJournalists.chooseTies import *

class validation(chooseTies):
	def __init__(self):
		chooseTies.__init__(self)
		self.simDict = {}
	
	# create simDict
	def createSimDict(self):
		j = 0
		for node1 in self.sections:
			j+=1
			print j,node1
			if self.sections[node1]:
				for node2 in self.sections:
					if self.sections[node2]:
						sim1 = self.cosSim(self.sections[node1], id2=node2)
						if sim1 > 0:
							self.simDict[(node1,node2)] = sim1

	# save simDict
	def saveSimDict(self, fname="simDict"):
		file = open(fname, "w")
		pickle.dump(self.simDict,file, -1)
		file.close()
	
	# load simDict if it has previously been calculated
	def loadSimDict(self, fname="simDict"):
		file = open(fname, "r")
		self.simDict = pickle.load(file)
		file.close()

	# count total number of correctly predicted followees
	def correctPred(self, K1=125):
		self.correctlyPredicted = 0
		self.returnTieStrength = False
		self.knownSimDict = True
		self.K1 = K1
		for node in self.sections:
			if self.sections[node]:
				self.egoToRemove = node
				self.run(node)
				noCorrectForNode = len(set(self.friendsList[node]).intersection(set(self.alters)))
				self.correctlyPredicted += noCorrectForNode




