#!/usr/bin/python -tt

import time
import urllib
from lxml import etree
from datetime import date, timedelta
import pymysql as mdb
import pickle
import sys
from addArticlesToSQL import *

class streamArticles():
	def __init__(self):
		# load files
		file = open("../app/static/friendsList", "r")
		self.friendsList = pickle.load(file)
		file.close()
		file = open("../app/static/topSections", "r")
		self.topSections = pickle.load(file)
		file.close()
		self.nodes = self.friendsList.keys()
		file = open("../app/static/key", "r")
		self.key = pickle.load(file)
		file.close()

	def openSQLconnection(self):
		self.con = mdb.connect('localhost', 'root', 'password', 'guardian')
		self.cur = self.con.cursor()

	def findRecentSections(self, i):
		self.sections = {}
		for node in self.nodes:
			self.cur.execute("SELECT section FROM articlesStream where id = "+node+" and date1 > "+str(i-7))
			rows = [row[0] for row in self.cur.fetchall()]
			self.sections[node] = []
			if rows:
				for row in rows:
					if row in self.topSections:
						self.sections[node] += [row]

	def saveSections(self, fname = "../app/static/sections"):
		file = open(fname, "w")
		pickle.dump(self.sections, file, -1)
		file.close()

	def recalculateSections(self, i):
		self.openSQLconnection()
		self.findRecentSections(i)
		self.saveSections()

	def getNewDate(self):
		t=time.strptime(self.oldDate,'%Y-%m-%d')
		newDate = date(t.tm_year,t.tm_mon,t.tm_mday)+timedelta(1)
		self.newDate = newDate.strftime('%Y-%m-%d')

	def getText(self, page):
		url = "http://content.guardianapis.com/search?format=xml&from-date="+self.oldDate+"&to-date="+self.newDate+"&show-tags=all&show-fields=all&show-refinements=all&api-key="+self.key+"&page-size=100&page="+str(page)
		#### dont need everything!!!
		page1 = urllib.urlopen(url)
		self.text = page1.read()

	def getNoPages(self):
		response = etree.fromstring(self.text)
		items = response.items()
		self.pages = 1
		for item in items:
			if item[0]=='pages':
				self.pages = int(item[1])

	def addArticles(self, date1):
		addArticlesToSQL(self.text, date1)


######################### MAIN #########################

def main():
	s = streamArticles()
	firstDate = sys.argv[1] # format '2015-02-02'
	start_i = int(sys.argv[2])
	s.oldDate = firstDate
	for i in xrange(start_i, 100):
		print i, s.oldDate
		s.getNewDate()
		s.getText(1)
		s.getNoPages()
		s.addArticles(i+1)
		print "Number of pages:", s.pages
		if s.pages > 1:
			# get other pages of articles
			for page in xrange(1,s.pages):
				s.getText(page+1)
				s.addArticles(i+1)
	
		# update sections for articles written in the past week
		s.recalculateSections(i)
		
		### go to sleep for a day
		s.oldDate = s.newDate
		print "Sleeping..."
		time.sleep(86400)


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
	main()















