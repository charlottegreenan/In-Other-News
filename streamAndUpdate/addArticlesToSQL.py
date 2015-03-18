#!/usr/bin/python -tt

import time
import urllib
from lxml import etree
from datetime import date, timedelta
import pymysql as mdb
import pickle
import sys

def addArticlesToSQL(text, date1):
	con = mdb.connect('localhost', 'root', 'password', 'guardian')
	cur = con.cursor()
	response = etree.fromstring(text)
	for results in response.iterchildren(): # one 'results' per response
		for result in results.iterchildren(): # 100 'result' per results
			url1=''
			section = ''
			title = ''
			contName = ''
			items = result.items() # finding the section of the article
			for item in items:
				if item[0]=='section-name':
					section = item[1]
				if item[0]=='web-title':
					title = item[1].encode('utf-8')
			for fieldsTags in result.iterchildren(): # 2 'fieldsTags' per result (either the fields or the tags
				if fieldsTags.tag == "tags":
					for tag in fieldsTags.iterchildren():
						items = tag.items()
						tagType = ''
						for item in items:
							if item[0]=='type':
								tagType = item[1]
						if tagType == 'contributor':
							contName = ''
							for item in items:
								if item[0]=='web-title':
									contName = item[1]
				if fieldsTags.tag == "fields":
					for field in fieldsTags.iterchildren():
						item = field.items()[0]
						if item[1]=="short-url":
							url1 = field.text
							print url1
			if contName:
				id = ''
				insert = False
				cur.execute('SELECT id from twitterHandles where name = "'+contName+'"')
				rows = cur.fetchall()
				if rows:
					id = rows[0][0] #?
				if id:
					insert = True
				if '"' in title and "'" in title:
					insert = False
				if '"' in title:
					values = "'"+str(id)+"','"+title+"','"+section+"','"+url1+"','"+str(date1)+"'"
				else:
					values = '"'+str(id)+'","'+title+'","'+section+'","'+url1+'","'+str(date1)+'"'
				if insert:
					command = "INSERT INTO articlesStream VALUES("+values+")"
					cur.execute(command)
	con.commit()
	con.close()
















