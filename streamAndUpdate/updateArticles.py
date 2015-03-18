#!/usr/bin/python -tt

import time
import urllib
from lxml import etree
from datetime import date, timedelta
import pymysql as mdb
import pickle
import sys
from streamArticles import *

######################### MAIN #########################

def main():
	s = streamArticles()
	firstDate = sys.argv[1] # format '2015-02-02'
	lastDate = sys.argv[2]
	start_i = int(sys.argv[3])
	s.oldDate = firstDate
	while s.oldDate != lastDate:
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
		i += 1

	# update sections for articles written in the past week
	s.recalculateSections(i)



# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
	main()















