import string
import simplejson
from datetime import datetime, timedelta
from email.utils import parsedate_tz
from twython import Twython
import datetime
from datetime import datetime
import pytz
import numpy as np
import datetime
from dateutil.parser import parse
from tweepy import StreamListener
from collections import defaultdict
import json, time, sys, unicodedata, operator, csv

#This function prints available account information.
#Saves the retrieved data to a 
#Takes Twython object and an array of twitter ids (usernames) as parameters
def retrieveaccountinfo(twitter, username):
	print('Retrieving account info from user with screen name \"' + username[0] + '\"...')
	twitter = twitter
	userinfo = []

	info = twitter.lookup_user(screen_name = username)
	userinfo.extend(info)
	savetojson(username[0], userinfo, '_info')

# Experimental function.
def testfunction(twitter, username):
	useddevices = []
	tweets = displaytweetjsonfile(username)
	checktweettimedifference(tweets)
	for tweet in tweets:
		if tweet['source'] == '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>' or tweet['source'] == '<a href="http://twitter.com" rel="nofollow">Twitter Web Client</a>':
			testnum = 1
		else:
			print(tweet['source'])

	#analyzeuseddevices(tweets)

# Experimental function.
def testfunctionextra(username):
	tweets = displaytweetjsonfile(username)
	devices = {}
	for tweet in tweets:
		#print(tweet['source'].partition('>')[-1].rpartition('<')[0])
		device = tweet['source'].partition('>')[-1].rpartition('<')[0]
		device = device.encode('utf8')
		
		if device in devices:
			devices[device] += 1
		else:
			devices[device] = 1

	print(devices)

# This function analyze dates of tweets and gathers tweets in dates so that one single
# date contains one or more tweets. Also saves this information in a file with format
# <username>_tweetdates.
def tweetsperdate(username):
	tweets = displaytweetjsonfile(username)
	dates = []
	datescount = {}
	datestamps = []

	for tweet in tweets:
		date = tweet['created_at']
		d = datetime.datetime.strptime(date, '%a %b %d %H:%M:%S +0000 %Y')
		date = d.strftime('%Y-%m-%d')
		datestamps.append(str(date))

	dates = [datetime.datetime.strptime(ts, "%Y-%m-%d") for ts in datestamps]
	dates.sort()
	sorteddates = [datetime.datetime.strftime(ts, "%Y-%m-%d") for ts in dates]

	for date in sorteddates:
		print(date)

	for date in sorteddates:
		if date in datescount:
			datescount[date] += 1
		else:
			datescount[date] = 1

	with open(username + '_tweetdates', 'w') as tf:
		for key in sorted(datescount):
			tf.write("%s: %s\n" % (key, datescount[key]))

# This function gathers tweet dates by device (source),
# and writes it to file with name "<username>_tweetdevices".
# Experimental!
def deviceperdate(username):
	tweets = displaytweetjsonfile(username)
	devicelist = []
	datelist = []
	datedevices = {}
	#datedevices['Twitter for Android'] = ['2017-03-20']
	#datedevices['Twitter for Android'].extend(['2016-03-02'])
	#print(datedevices)

	#devicelist = ['Twitter for Android']
	for tweet in tweets:
		device = tweet['source'].partition('>')[-1].rpartition('<')[0]
		device = device.encode('utf8')
		if device not in devicelist:
			devicelist.append(device)
	for item in devicelist:
		datedevices[item] = ['1980-05-20']

	print(devicelist)
	print(datedevices)
	for tweet in tweets:
		date = tweet['created_at']
		d = datetime.datetime.strptime(date, '%a %b %d %H:%M:%S +0000 %Y')
		date = d.strftime('%Y-%m-%d')
		datelist.append(date)
		device = tweet['source'].partition('>')[-1].rpartition('<')[0]
		device = device.encode('utf8')

		#print(type(datedevices[device]))
		if device in datedevices:
			datedevices[device].extend([date])
		else:
			datedevices[device] = date
	for item in datedevices.itervalues():
		try:
			item.remove('1980-05-20')
		except ValueError:
			pass

	dates = [datetime.datetime.strptime(ts, "%Y-%m-%d") for ts in datelist]
	dates.sort()
	sorteddates = [datetime.datetime.strftime(ts, "%Y-%m-%d") for ts in dates]

	#print(datedevices)
	#print(datedevices)
	with open(username + '_tweetdevices', 'w') as tf:
		for key in sorted(datedevices):
			print(key + str(datedevices[key]))
			tf.write('\n' + key + str(datedevices[key]))
	savedicttocsv(username, datedevices)

	print(sorteddates[0] + ' and ' + sorteddates[len(sorteddates) - 1])

	print(datedevices['Twitter for iPad'])

	for key in sorted(datedevices):
		savetocsv(username, datedevices[key], key)
		#print(datedevices[key])

# This function saves device -and date information to a csv-file.
def savetocsv(username, datenumbers, device):
	datedict = {}
	datenumbers.sort()
	for key in sorted(datenumbers):
		if key in sorted(datedict):
			datedict[key] += 1
		else:
			datedict[key] = 1
	#datedict['2017-03-13'] = 1
	print('________________________')
	print(datenumbers)
	print('________________________')
	print(datedict)

	with open(username + '_' + device, 'w') as tf:
		writer = csv.writer(tf)
		#print(datenumbers)
		for key in datedict:
			writer.writerow( str((key)).split(',') + str((datedict[key])).split(',') )
			#writer.writerow( str((datedict[key])).split(',') )



def savedicttocsv(username, datedevices):
	devicelist = []
	for key in sorted(datedevices):
		devicelist.append(key)
	counter = 0

	datedevicenumdict = {}
	ddnumtest = {"1980-05-20": 5}
	datedevicenumdict["Test"] = ddnumtest
	#print(datedevicenumdict)
	for key in datedevices:
		for date in datedevices[key]:
			if key in datedevicenumdict:
				if date in datedevicenumdict[key]:
					datedevicenumdict[key][date] += 1
				else:
					datedevicenumdict[key][date] = 1
			else:
				tempdict = {date: 1}
				datedevicenumdict[key] = tempdict
			#print(datedevicenumdict)
	#del datedevicenumdict['Test']
	print(datedevicenumdict)


	with open(username + '_tweetdevices.csv', 'w') as tf:
		writer = csv.writer(tf)
		for key in devicelist:
			writer.writerow( str((key)).split(',') )
			length = len(datedevices[key])
			while counter < len(datedevices[key]):
				writer.writerow( str((datedevices[key][counter])).split(',') )
				counter += 1
			counter = 0


def analyzeuseddevices(tweets):
	for tweet in tweets:
		print(tweet['source'])

#This function reads a file with tweets as json data and displays it.
def displaytweetjsonfile(username):
	json_data = {}
	with open(username + '_alltweets.json') as file:
		json_data = file.read()
	arr = json.loads(json_data)
	#for tweet in arr:
	#	print(tweet)
	print(len(arr))
	#print(arr[0]['created_at'])
	return arr

#This function reads a file with user info as json data and displays it.
def displayuserinfojsonfile(username):
	json_data = {}
	with open(username + '_info.json') as file:
		json_data = file.read()
	arr = json.loads(json_data)
	print(arr[0]['created_at'])

#This function will pull the last 3,200 (approximately) tweets of a user and saves it to a json-file with format <username>_alltweets.json. Starting at the last tweet.
#Takes a Twython object and a username (array) as parameters.
#Supposedly, it is needed to wait for 300 seconds per 200 requests. But i have tested this without waiting, and it works just fine.
def getalltweets(twitter, username):
	print('Getting the last 3,200 tweets from user \"' + username[0] + '\"')
	lasttweet = twitter.get_user_timeline(screen_name=username[0], count=1, include_retweets=False)
	lis = lasttweet[0]['id']
	tweets = []
	for i in range(0, 16):
		print('Downloading tweets...')
		user_timeline = twitter.get_user_timeline(screen_name=username[0], count=200, include_retweets=False, max_id = lis)
		print('200 tweets fetched!')
		for tweet in user_timeline:
			#print(tweet['text'])
			lis = tweet['id']
		#print('Waiting for 300 seconds...')
		#time.sleep(300)
		tweets.extend(user_timeline)
	savetojson(username[0], tweets, '_alltweets')

#This function calculate and return the daily average of tweets. This is
#based on the number of tweets a user have and for how many days the account
#have been registered (tweetcount divided by days since the account was created).
#This function return the calculated daily average number of tweets.
def calcavgtweets(statuses_count, created_at):
	return statuses_count / daysregistered(created_at)

#This function calculate the number of days since an account were registered.
#Does not take leap years in precaution.
#Returns the number of days since the account was created (float).
def daysregistered(created_at):
	return ((to_sdatetime(datetime.datetime.now().strftime('%a %b %d %H:%M:%S +0000 %Y')) - datetime.datetime.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')).total_seconds() / (24*60*60))

def checktweettimedifference(tweets):
	counter = 0
	datelist = []
	difference = []

	while (counter < len(tweets) - 1):
		if (counter < len(tweets) - 1):
			tweettimea = datetime.datetime.strptime(tweets[counter]['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
			tweettimeb = datetime.datetime.strptime(tweets[counter + 1]['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
			delta = tweettimea - tweettimeb
			datelist.append(delta)
			print(str(counter))

			datelist[counter] = datetime.datetime.strptime(tweets[counter]['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
		counter += 1
	counter = 0

	max = datelist[0] - datelist[1]
	min = datelist[1] - datelist[2]
	while (counter < len(datelist) - 1):
		if datelist[counter] - datelist[counter + 1] > max:
			max = datelist[counter] - datelist[counter + 1]
		elif datelist[counter] - datelist[counter + 1] < min:
			min = datelist[counter] - datelist[counter + 1]
		counter += 1

	print('Maximum time difference = ' + str(max))
	print('Minimum time difference = ' + str(min))

#This function prints the largest and smallest time difference between tweets
#Takes a Twython object and array of ids (usernames) as parameters.
def checktweetdifference(twitter, ids):
	twitter = twitter
	useridlist=[]
	counter = 0
	datelist = []
	difference = []

	for username in ids:
		useridlist.append(fromnametoid(twitter, username))

	print('Checking time difference of tweets for user ' + ids[0] + ' (' + useridlist[0] + ')')

	#Getting the timeline
	user_timeline = twitter.get_user_timeline(user_id=useridlist[0])

	for tweet in user_timeline:
		print(tweet['created_at'])

	while (counter < len(user_timeline) - 1):
		if counter < len(user_timeline) - 1:
			tweettimea = datetime.datetime.strptime(user_timeline[counter]['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
			tweettimeb = datetime.datetime.strptime(user_timeline[counter + 1]['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
			delta = tweettimea - tweettimeb
			datelist.append(delta)

			datelist[counter] = datetime.datetime.strptime(user_timeline[counter]['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
			counter += 1

	counter = 0

	max = datelist[0] - datelist[1]
	min = datelist[1] - datelist[2]
	while (counter < len(datelist) - 1):
		if datelist[counter] - datelist[counter + 1] > max:
			max = datelist[counter] - datelist[counter + 1]
		elif datelist[counter] - datelist[counter + 1] < min:
			min = datelist[counter] - datelist[counter + 1]
		counter += 1

	print('Maximum time difference = ' + str(max))
	print('Minimum time difference = ' + str(min))

#This function displays a given user's latest tweets.
#Prints 20 tweets as default.
def gettweetsampleset(twitter, username):
	user_timeline = twitter.get_user_timeline(screen_name=username[0])
	for tweet in user_timeline:
		#print(tweet['text'])
		#print('_____________________________________')
		savetweettojson(username[0], tweet, '_tweetsample')

#This function saves parameter data (json) to file.
#Filename used is in following format: username_type.json where type is a filename format.
def savetojson(username, data, type):
	print('Saving json data to filename \"' + username + type + '.json\"...')
	with open(username + type + '.json', 'a') as tf:
		json.dump(data, tf)
	print(str(len(data)) + ' entries written')

#This function saves tweet data as json data  in a file.
#Filename used is in following format: username_type.json where type is a filename format.
def savetweettojson(username, tweet, type):
	tweetdata = {}
	tweetdata['contributors'] = tweet['contributors']
	tweetdata['coordinates'] = tweet['coordinates']
	tweetdata['created_at'] = tweet['created_at']
	#tweetdata['current_user_retweet'] = tweet['current_user_retweet']
	tweetdata['entities'] = tweet['entities']
	tweetdata['favorite_count'] = tweet['favorite_count']
	tweetdata['favorited'] = tweet['favorited']
	#tweetdata['filter_level'] = tweet['filter_level']
	tweetdata['geo'] = tweet['geo']
	tweetdata['id'] = tweet['id']
	tweetdata['id_str'] = tweet['id_str']
	tweetdata['in_reply_to_screen_name'] = tweet['in_reply_to_screen_name']
	tweetdata['in_reply_to_status_id'] = tweet['in_reply_to_status_id']
	tweetdata['in_reply_to_status_id_str'] = tweet['in_reply_to_status_id_str']
	tweetdata['in_reply_to_user_id'] = tweet['in_reply_to_user_id']
	tweetdata['in_reply_to_user_id_str'] = tweet['in_reply_to_user_id_str']
	tweetdata['lang'] = tweet['lang']
	tweetdata['place'] = tweet['place']
	#tweetdata['possibly_sensitive'] = tweet['possibly_sensitive']
	#tweetdata['quoted_status_id'] = tweet['quoted_status_id']
	#tweetdata['quoted_status_id_str'] = tweet['quoted_status_id_str']
	#tweetdata['quoted_status'] = tweet['quoted_status']
	#tweetdata['scopes'] = tweet['scopes']
	tweetdata['retweet_count'] = tweet['retweet_count']
	tweetdata['retweeted'] = tweet['retweeted']
	#tweetdata['retweeted_status'] = tweet['retweeted_status']
	tweetdata['source'] = tweet['source']
	tweetdata['text'] = tweet['text']
	tweetdata['truncated'] = tweet['truncated']
	tweetdata['user'] = tweet['user']
	#tweetdata['witheld_copyright'] = tweet['witheld_copyright']
	#tweetdata['witheld_in_countries'] = tweet['witheld_in_countries']
	#tweetdata['witheld_scope'] = tweet['witheld_scope']

	with open(username + type + '.json', 'a') as tf:
		json.dump(tweetdata, tf)

#This function returns json data read from a file.
#Filename used is in following format: username_type.json where type is a filename format.
def readtweetfromjson(username, type):
	read_json = {}
	with open(username + type + '.json', 'r') as tf:
		read_json = json.loads(tf)
	return read_json

#This function returns json data read from a file.
#Takes string (username) and string (datatype format).
#Datatype format is just a format for the filename.
def readfromjson(username, type):
	read_json = {}
	with open(username + type + '.json', 'r') as tf:
		read_json = json.load(tf)
	return read_json

#This function returns the id of a twitter account by username.
#Takes a Twython object and array with username as parameters.
def fromnametoid(twitter, username):
	twitter = twitter
	output = twitter.lookup_user(screen_name=username)

	userid_list=[]

	userid = output[0]['id_str']

	return userid

#This function returns the username of a twitter account by a given id.
#Takes a Twython object and array with id as parameters.
def fromidtoname(twitter, id):
	twitter = twitter
	output = twitter.lookup_user(user_id=id)

	usernamelist = []

	return str(output[0]['screen_name'])

#This function returns a detetime-object based on a string.
#Takes a string as a parameter.
def to_sdatetime(datestring):
	return datetime.datetime.strptime(datestring, '%a %b %d %H:%M:%S +0000 %Y')

#A Twitter StreamListener class implementing StreamListener from the tweepy library.
#The fetched tweets is stored in a file called 'fetched_tweets.txt'
class SListener(StreamListener):
	def on_status(self, status):
		print(status.text)

	def on_data(self, data):
		print('Data received!')
		with open('fetched_tweets1.txt', 'a') as tf:
			tf.write(data)
		return True

	def on_error(self, status_code):
		print status_code
		return False