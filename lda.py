from pymongo import MongoClient
from nltk.tokenize import RegexpTokenizer
import gensim
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from gensim import corpora,models
import numpy as np
import pyLDAvis
import pyLDAvis.gensim
#import pyLDAvis.graphlab
stop = stopwords.words("english")

def strip_proppers_POS(text):
	#text = text.encode('ascii','ignore')
	tagged = pos_tag(text.split()) #use NLTK's part of speech tagger
	non_adj = [word for word,pos in tagged if pos[0] != 'J' and word not in stop and len(word) > 3]
	master = ""
	for i in non_adj:
		if (i[0] == '@'):
			i = i.lstrip('@')
		if (i[0] == '#'):
			i = i.lstrip('#')
		if i[:4] == 'http':
			continue
		master = master+i+" "
	return master


client = MongoClient('mongodb://localhost:27017')
db = client.epidemic
user_tweets = db.user_tweets
topic_tweets = db.topic_tweets

def lda_topic(topic):
	tweets_db = topic_tweets.find({'topic':topic})
	tweets = []
	for i in tweets_db:
		for j in i['tweets']:
			tweets.append(j.lower())
	refined_tweets = []
	c=0
	for t in tweets:
		refined_tweets.append(strip_proppers_POS(t))
	
	return refined_tweets
	# tokenizer = RegexpTokenizer(r'\w+')
	# texts = []
	# for i in range(0,len(refined_tweets)):
	# 	texts.append(tokenizer.tokenize(refined_tweets[i]))
	# keywordArray = []
	# dictionary = corpora.Dictionary(texts)
	# dictionary.filter_extremes(no_below=2, no_above=0.8)
	# corpus = [dictionary.doc2bow(text) for text in texts]

	
	# m = models.LdaModel(corpus,id2word=dictionary,num_topics=20,update_every=5,chunksize=10000,passes=10)
	# topics_matrix = m.show_topics(formatted=True, num_words=5)
	# topics_matrix = np.array(topics_matrix)
	# for i in range(0,20,1):
	# 	print topics_matrix[i,1]

	#keywordArray = topics_matrix[:,:,1]
	#keywordArrayProb = topics_matrix[:,:,0]
	
	#p = pyLDAvis.gensim.prepare(m,corpus,dictionary)
	#pyLDAvis.show(p)


def lda_user(doctors):
	tweets = []
	for doctor in doctors:
		print doctor
		tweets_db = user_tweets.find({'screen_name':doctor})
		for i in tweets_db:
			tCount = 0
			for j in i['tweets']:
				if tCount < 10:
					tweets.append(j.lower())
					tCount += 1
					print tCount
				else:
					break
		refined_tweets = []
		c=0
		for t in tweets:
			refined_tweets.append(strip_proppers_POS(t))
		print 'done!'
	return refined_tweets

def lda(doctors, topic):
	
	refined_tweets = lda_user(doctors)
	refined_tweets += lda_topic(topic)

	tokenizer = RegexpTokenizer(r'\w+')
	texts = []
	for i in range(0,len(refined_tweets)):
		texts.append(tokenizer.tokenize(refined_tweets[i]))
	keywordArray = []
	dictionary = corpora.Dictionary(texts)
	dictionary.filter_extremes(no_below=2, no_above=0.8)
	corpus = [dictionary.doc2bow(text) for text in texts]

	
	m = models.LdaModel(corpus,id2word=dictionary,num_topics=3,update_every=5,chunksize=10000,passes=10)
	topics_matrix = m.show_topics(formatted=True, num_words=5)
	topics_matrix = np.array(topics_matrix)
	#for i in range(0,20,1):
	#	print topics_matrix[i,1]

	#keywordArray = topics_matrix[:,:,1]
	#keywordArrayProb = topics_matrix[:,:,0]
	
	p = pyLDAvis.gensim.prepare(m,corpus,dictionary)
	pyLDAvis.show(p)



if __name__ == '__main__':
	#lda_topic('#zika')
	#doctors = ['GlenGilmore','RRuth_TSG','StemCellsGlobal','kevinmd','AmerMedicalAssn','RedCross','lescat','ahier','PatientDave','drwalker_rph','PhilBaumann','Health_Affairs','jensmccabe','nursefriendly','lindner_sarah','CHopeMurray','Kamiyamay','OhMyJet','bigzigfitness','giasison','ElinSilveous','GailZahtz','NatriceR','going2medschool','CSlaterMD','andyhubbard','drseisenberg','LAlupusLady','ChatHealth','MandiBPro','RockScarLove','bigfish','MarksPhone','aptainaccess','NAMIOC','ChronicPainGPS','RannPatterson','CortLane','arter4values','Saif_Abed','Mass_Consumer','DrLeanaWen','gordondeb','AtriusHealth','YoungHealthPros','CrystalLaw','althhashtags','ashingtonpost','_NetworkHealth','juscohen']	
	doctors = ['GlenGilmore','RRuth_TSG','StemCellsGlobal','kevinmd','AmerMedicalAssn','RedCross']	
	lda(doctors, "#zika")
	
