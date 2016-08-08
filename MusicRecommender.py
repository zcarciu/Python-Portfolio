import json, re, sys, os
import musicbrainzngs as mbz


mbz.set_useragent('course-project', '1.0', 'zcarciu@albany.edu')


def main():
	if len(sys.argv) != 2:
		print "Usage: \n$ python MusicRecommender.py <raw-tweets-file>"
		sys.exit()
	else:
		recommender = Recommender(sys.argv[1])
	try:
		foo = recommender.make_association_rules()
	except mbz.musicbrainz.ResponseError:
		print "A response error has occurred!"


class Recommender:
	def __init__(self, raw_tweet_file_name):

		self.raw_tweet_file = raw_tweet_file_name

		########### make folder to keep data
		########### and intermediate files
		if not os.path.exists('data'):
			os.mkdir('data')
		raw_tweet_file = sys.argv[1]

	def clean_raw_tweets(self):
		print "Cleaning raw tweets from", self.raw_tweet_file
		cleaned_tweets = []
		tweet_count = 0
		with open(self.raw_tweet_file, 'r') as f:
			for line in f.readlines():
					
				if "****" not in line:
					new_tweet = dict()
					try:
						tweet = json.loads(line)
						tweet['text'] = re.sub('https:.*|&amp;', '', tweet['text'])
						tweet['text'] = re.sub('(?i)#nowplaying|(?i)#iheartradio', '', tweet['text'])
						tweet['text'] = re.sub('(?i)#listeningto|(?i)@tunein', '', tweet['text'])
						new_tweet['text'] = tweet['text']
						new_tweet['userID'] = tweet['user']['id']
						new_tweet['tweetID'] = tweet['id']
						cleaned_tweets.append(new_tweet)
						tweet_count += 1
						print tweet_count
					except (KeyError, ValueError):
						pass

		print "Read/Cleaned in %s tweets" % (tweet_count)
		return cleaned_tweets, tweet_count


	############ cleaned_tweets is a list of json entries
	############ cleaner_tweets will have songs assigned
	############ to tweets
	def assign_songs(self, cleaned_tweets):
		print "Matching songs to tweets"
		cleaner_tweets = []
		tweets_used = 0
		for cleaned_tweet in cleaned_tweets:
			if " by " in cleaned_tweet['text']:
				split_text = cleaned_tweet['text'].split(' by ')
				artists_list = mbz.search_artists(split_text[0])
				try:
					mbID = artists_list['artist-list'][0]['id']
					works = mbz.search_recordings(query=split_text[0],
															arid=mbID)
					tweet = dict()	
					tweet['song'] = works['recording-list'][0]['title']
					tweet['text'] = cleaned_tweet['text']
					tweet['artist'] = artists_list['artist-list'][0]['name']
					tweet['musicbrainzID'] = works['recording-list'][0]['id']
					tweet['userID'] = cleaned_tweet['userID']
					cleaner_tweets.append(tweet)
					tweets_used += 1

				except (UnicodeEncodeError, IndexError):
					print "Unable to find song/artist"
		
		print "Tweets used: %s" % (tweets_used)
		return cleaner_tweets


	def assign_user_info(self, cleaner_tweets):
		user_songs = dict()
		user_artists = dict()

		for tweet in cleaner_tweets:
			userID = tweet['userID']
	
			if user_songs.has_key(userID):
				user_songs[userID].append(tweet['song'])
			else:
				user_songs[userID] = [tweet['song']]
	
			if user_artists.has_key(userID):
				user_artists[userID].append(tweet['artist'])
			else:
				user_artists[userID] = [tweet['artist']]
			
		users = [] 
		user = dict()
		for key in user_songs.keys():
			user['userID'] = key
			user['songs'] = user_songs[key]
			user['artists'] = user_artists[key]
			users.append(user)
		return users


	def make_association_rules(self):
		cleaned_tweets, tweet_count = self.clean_raw_tweets()		
		cleaner_tweets = self.assign_songs(cleaned_tweets)
		users = self.assign_user_info(cleaner_tweets)
		print users

		##########################
		####### association rules code will go here
		
			

	

	
		

if __name__ == '__main__':
	main()
