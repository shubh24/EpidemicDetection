from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
import matplotlib.pyplot as plt

db = client.epidemic
user_tweets = db.user_tweets
topic_tweets = db.topic_tweets

if __name__ == '__main__':
	dengue = topic_tweets.find_one({'topic':'#dengue'})['created_at']
	zika = topic_tweets.find_one({'topic':'#zika'})['created_at']

	d_dict = {}
	for i in dengue:
		if int(i) not in d_dict:
			d_dict[int(i)] = 1
		else:
			d_dict[(int(i))] += 1


	z_dict = {}
	for i in zika:
		if int(i) not in z_dict:
			z_dict[int(i)] = 1
		else:
			z_dict[(int(i))] += 1

	import operator
	d_dict = sorted(d_dict.items(), key=operator.itemgetter(0))
	z_dict = sorted(z_dict.items(), key=operator.itemgetter(0))
	
	res = {'#dengue' : d_dict, '#zika': z_dict}
	
	colors = list("rgbcmyk")
	
	for r in res.values():
		x = [i[0] for i in r]
		y = [i[1] for i in r]
		plt.plot(x,y, '-o', color=colors.pop())
	
	plt.legend([i for i in res])	
	plt.show()