from pymongo import MongoClient
from nltk.tokenize import RegexpTokenizer
import gensim
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from gensim import corpora,models
import numpy as np
#import pyLDAvis
#import pyLDAvis.gensim
#import pyLDAvis.graphlab
stop = stopwords.words("english")

def strip_proppers_POS(text):
	#text = text.encode('ascii','ignore')
	tagged = pos_tag(text.split()) #use NLTK's part of speech tagger
	non_adj = [word for word,pos in tagged if pos != 'JJ' and pos != 'JJR' and pos != 'JJS' and word not in stop]
	master = ""
	for i in non_adj:
		if (i[0] == '@'):
			i = i.lstrip('@')
		if (i[0] == '#'):
			i = i.lstrip('#')
		if i[:4] == 'http':
			continue
		if len(i) > 3:
			master = master+i+" "
	return master


client = MongoClient('mongodb://localhost:27017')
db = client.epidemic
user_tweets = db.user_tweets
topic_tweets = db.topic_tweets

def lda_vis(topic):
	tweets_db = topic_tweets.find({'topic':topic})
	tweets = []
	for i in tweets_db:
		for j in i['tweets']:
			tweets.append(j.lower())
	refined_tweets = []
	c=0
	for t in tweets:
		refined_tweets.append(strip_proppers_POS(t))
	
	tokenizer = RegexpTokenizer(r'\w+')
	texts = []
	for i in range(0,len(refined_tweets)):
		texts.append(tokenizer.tokenize(refined_tweets[i]))
	keywordArray = []
	dictionary = corpora.Dictionary(texts)
	dictionary.filter_extremes(no_below=2, no_above=0.8)
	corpus = [dictionary.doc2bow(text) for text in texts]

	
	m = models.LdaModel(corpus,id2word=dictionary,num_topics=5,update_every=5,chunksize=10000,passes=10)
	topics_matrix = m.show_topics(formatted=True, num_words=5)
	topics_matrix = np.array(topics_matrix)
	for i in range(0,5,1):
		print topics_matrix[i,1]

	#keywordArray = topics_matrix[:,:,1]
	#keywordArrayProb = topics_matrix[:,:,0]
	
	#p = pyLDAvis.gensim.prepare(m,corpus,dictionary)
	#pyLDAvis.show(p)



if __name__ == '__main__':
	lda_vis('#zika')
