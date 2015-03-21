#!/usr/bin/python -tt

from chooseJournalists.chooseTies import *
from useSQL import *

class recommendations(chooseTies, useSQL):
	def runFinal(self, list):
		self.returnTieStrength = True
		self.run(list)
		self.startSQLconnection()
		self.findMaxDate()
		self.altersDict = dict(self.alters)
		self.handlesDict = {} # for each journalist returns their twitter handle
		self.articlesDict = {} # for each journalist, list of articles.  Each article has title, section, url, colour
		found = dict([(sect, False) for sect in self.topSections])
		self.alters2 = []
		if self.alters:
			for date in xrange(self.maxDate,-1,-1):
				if sum([not item[1] for item in found.items()]):
					for alter1 in self.alters:
						alter = alter1[0]
						self.getArticles(alter, date)

						# recommend articles that are from sections we haven't yet
						# got a recommendation for
						for i in xrange(len(self.articles)):
							title1 = self.articles[i][1]
							sect = self.articles[i][2]
							url1 = self.articles[i][3]
							if sect in self.topSections:
								if not found[sect]:
									if alter in self.articlesDict:
										self.articlesDict[alter] += [[title1, sect, url1, self.colorMap[sect]]]
									else:
										self.articlesDict[alter] = [[title1, sect, url1, self.colorMap[sect]]]
									if alter not in self.handlesDict:
										self.handlesDict[alter] = [self.handle]
									found[sect] = True
									if alter1 not in self.alters2:
										self.alters2 += [alter1]

		# sort journalists, firstly by tie strength, and then by indegree
		self.sortedJournalists = [s[0] for s in sorted(self.alters2, key=self.mykey2,reverse=True)]

	def getArticles(self, alter, date):
		# get twitter handle
		self.cur.execute("SELECT name, screen_name, id FROM twitterHandles where id ="+alter)
		self.handle = self.cur.fetchall()[0]
				
		# get articles written by alter on date
		self.cur.execute("SELECT * FROM articlesStream where id ="+alter+" and date1 = "+str(date))
		self.articles = self.cur.fetchall()

########################## MAIN FUNCTION ############################
def main(mySections, excludedNodes, myties):
	r = recommendations()
	r.myties = myties
	r.excludedNodes = excludedNodes
	r.runFinal(mySections)

	return [r.handlesDict, r.articlesDict, r.sortedJournalists]








