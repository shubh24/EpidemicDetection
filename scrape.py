import sys
import string
import simplejson
from twython import Twython

import datetime
now = datetime.datetime.now()
day=int(now.day)
month=int(now.month)
year=int(now.year)

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client.epidemic
user_tweets = db.user_tweets
topic_tweets = db.topic_tweets

t = Twython(app_key='yOc6qbMtrTRJ5QmHpy640yCS9', app_secret='4mPSvT4y7T3auJA3Z5iytIIRdvKMnOqJug4fHTqeakf5wh4bo0', oauth_token='2892300355-9xhU0WMC91WRUjT80r8mzmrBIUOI9gMfcN7tvuB', oauth_token_secret='TNZ06Pt8hS2OYCVfDDJ1YnP4qQQYkFzL9FaxSptZWFJgk')
   

#REPLACE WITH YOUR LIST OF TWITTER USER IDS
#ids = "207442453,"
#users = t.lookup_user(user_id = ids)

def get_user_timeline(screen_name):
	tweets = t.get_user_timeline(screen_name=screen_name)
	res = {}
	res['screen_name'] = screen_name
	res['tweets'] = [i['text'] for i in tweets]
	user_tweets.insert_one(res)

def get_topic_tweets(topic, count):
	tweets = t.search(q=topic, count = count,language="en")
	collections = tweets['statuses']
	res = {}
	res['topic'] = topic
	res['tweets'] = [i['text'] for i in collections]
	topic_tweets.insert_one(res)	

if __name__ == '__main__':
	#get_user_timeline('mashable')
	get_topic_tweets('#zika',100)
