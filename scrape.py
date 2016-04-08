from __future__ import division
import sys
import string
import simplejson
from twython import Twython
import config
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

t = Twython(app_key=config.app_key, app_secret=config.app_secret, oauth_token=config.oauth_token, oauth_token_secret=config.oauth_token_secret)
   

#REPLACE WITH YOUR LIST OF TWITTER USER IDS
#ids = "207442453,"
#users = t.lookup_user(user_id = ids)

def get_user_timeline(screen_name):
	for screen_name in doctors:
		try:
			print screen_name
			tweets = t.get_user_timeline(screen_name=screen_name)
			res = {}
			res['screen_name'] = screen_name
			res['tweets'] = [i['text'] for i in tweets]
			user_tweets.insert_one(res)
			print 'inserted'		
		except:
			print 'Error from Twython' + screen_name
			pass

def get_topic_tweets(topic, count):
	tweets = t.search(q=topic, count = count,language="en")
	collections = tweets['statuses']
	res = {}
	res['topic'] = topic
	res['created_at'] = [int(i['created_at'][11:13]) for i in collections]
	res['screen_name'] = [i['user']['screen_name'] for i in collections]
	res['tweets'] = [i['text'] for i in collections]
	topic_tweets.insert_one(res)	


def get_official_ratio(topic, doctors):
	collections = topic_tweets.find({'topic':topic})
	official_count = 0
	total_count = 0
	for s in collections:
		tweeters = s['screen_name']
		for t in tweeters:
			if t in doctors:
				official_count += 1
			total_count += 1
	return official_count/total_count

if __name__ == '__main__':
	doctors = ['99Pastimes','GlenGilmore','RRuth_TSG','StemCellsGlobal','kevinmd','AmerMedicalAssn','RedCross','lescat','ahier','PatientDave','drwalker_rph','PhilBaumann','Health_Affairs','jensmccabe','nursefriendly','lindner_sarah','CHopeMurray','Kamiyamay','OhMyJet','bigzigfitness','giasison','ElinSilveous','GailZahtz','NatriceR','going2medschool','CSlaterMD','andyhubbard','drseisenberg','LAlupusLady','ChatHealth','MandiBPro','RockScarLove','bigfish','MarksPhone','aptainaccess','NAMIOC','ChronicPainGPS','RannPatterson','CortLane','arter4values','Saif_Abed','Mass_Consumer','DrLeanaWen','gordondeb','AtriusHealth','YoungHealthPros','CrystalLaw','althhashtags','ashingtonpost','_NetworkHealth','juscohen']
	#get_user_timeline(doctors)
	get_topic_tweets('#zika',1000)
	get_topic_tweets('#dengue',1000)


	#print get_official_ratio('#zika', doctors)