#!/usr/bin/python -tt

import pymysql as mdb
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle


####
#### functions
####

## Angular similarity instead of cosine
def angSim(list, id2 = '29441056'):
	sim2 = 1 - 2 * np.arccos(cosSim(list, id2))/ np.pi
	return sim2

## Find the mode of a list
def listMode(list1):
	return sorted([(list1.count(i),i) for i in list1])[-1][1]

####
#### initialize class
####

class initialize():
	def __init__(self):
		self.loadFiles()
		self.createColorMap()
		self.findIndegrees()
		self.myties = []
		self.excludedNodes = []
	
	def loadFiles(self):
		file = open("app/static/friendsList", "r")
		self.friendsList = pickle.load(file)
		file.close()
		file = open("app/static/sections", "r")
		self.sections = pickle.load(file)
		file.close()
		self.nodes = self.sections.keys()
		file = open("app/static/topSections", "r")
		self.topSections = pickle.load(file)
		file.close()

	def createColorMap(self):
		self.colorMap = {}
		self.colorMap['Business'] = '#BFBFBF'
		self.colorMap['Football'] = '#BFBFFF'
		self.colorMap['World news'] = '#BFFFBF'
		self.colorMap['Comment is free'] = '#FFBFBF'
		self.colorMap['Sport']  = '#BFFFFF'
		self.colorMap['Music'] = '#FFBFFF'
		self.colorMap['Technology'] = '#FFFFBF'
		self.colorMap['Life and style'] = '#FFFFFF'

	def findIndegrees(self): # can do with a Counter
		self.inties = {}
		for node in self.nodes:
			self.inties[node] = 0
		for node in self.nodes:
			if self.friendsList[node]:
				for alter in self.friendsList[node]:
					self.inties[alter] += 1

	## Find cosine similarity between a journalist id2 and a user with preferences
	## given by list1
	def cosSim(self, list1, id2 = '185583012'):
		if id2 in self.sections:
			list2 = self.sections[id2]
		else:
			list2 = ['']
		list3 = np.unique(list1 + list2)
		a = [list1.count(i) for i in list3]
		b = [list2.count(i) for i in list3]
		return cosine_similarity(a,b)[0][0]

	def mykey2(self, item):
		return (item[1], self.inties[item[0]])


