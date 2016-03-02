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
	res['tweets'] = [i['text'] for i in collections]
	topic_tweets.insert_one(res)	

if __name__ == '__main__':
	doctors = ['GlenGilmore','RRuth_TSG','StemCellsGlobal','kevinmd','AmerMedicalAssn','RedCross','lescat','ahier','PatientDave','drwalker_rph','PhilBaumann','Health_Affairs','jensmccabe','nursefriendly','lindner_sarah','CHopeMurray','Kamiyamay','OhMyJet','bigzigfitness','giasison','ElinSilveous','GailZahtz','NatriceR','going2medschool','CSlaterMD','andyhubbard','drseisenberg','LAlupusLady','ChatHealth','MandiBPro','RockScarLove','bigfish','MarksPhone','aptainaccess','NAMIOC','ChronicPainGPS','RannPatterson','CortLane','arter4values','Saif_Abed','Mass_Consumer','DrLeanaWen','gordondeb','AtriusHealth','YoungHealthPros','CrystalLaw','althhashtags','ashingtonpost','_NetworkHealth','juscohen']
	get_user_timeline(doctors)
	#get_topic_tweets('#zika',100)
