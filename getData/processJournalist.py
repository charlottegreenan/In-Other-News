#!/usr/bin/python -tt

import re
import tweepy
from lxml import etree
import pickle

## get twitter handle, id and list of friends for new journalist
class processJournalist(name, bio):
	def __init__(self):
		self.name = name
		self.bio = bio
		self.handle = ''
		self.id = '' # str or int?
		self.getHandleFromGuardianBio()
		self.connectToTwitterApi()
		if self.handle:
			self.getId()
		else:
			self.searchByName()
		if self.id:
			self.getFriends()

	def getHandleFromGuardianBio(self):
		handles = re.findall('twitter.com\/(\w+)"', self.bio)
		if handles:
			self.handle = handles[0]

	def connectToTwitterApi(self,fname="twitterTokens"):
		file = open(fname, "r")
		consumer_key, consumer_secret, access_token, access_token_secret = pickle.load(file)
		file.close()
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.secure = True
		auth.set_access_token(access_token, access_token_secret)
		self.api = tweepy.API(auth)

	# find id if we have handle
	def getId(self):
		try:
			userInfo = self.api.get_user(self.handle)
			self.id = userInfo.id
		except:
			print 'Error: could not find user with this handle.'

	# search twitter for users using name, if we couldn't get handle from bio
	def searchByName(self):
		searchTerms = ['guardian', 'observer', 'journalist', 'author', 'column', 'writer']
		userSearch = self.api.search_users(user)
		found = False
		for user in userSearch:
			if not found:
				json = user._json
					if 'description' in json and not found:
						desc = json['description'].lower()
						gu = any([re.findall(s, desc) for s in searchTerms])
						if gu:
							found = True
							self.id = user.id
							self.handle = user.screen_name

	def getFriends(self):
		self.friends = self.api.friends_ids(self.id) #id as string?

