#!/usr/bin/python -tt

import pymysql as mdb

class useSQL():
	def startSQLconnection(self):
		con = mdb.connect('localhost', 'root', 'password', 'guardian')
		self.cur = con.cursor()

	def findMaxDate(self):
		self.cur.execute("SELECT max(date1) FROM articlesStream")
		self.maxDate = int(self.cur.fetchall()[0][0])











