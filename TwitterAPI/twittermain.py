from twython import *
from retrieve_twitter_info import retrieveaccountinfo
from retrieve_twitter_info import checktweetdifference
from retrieve_twitter_info import fromnametoid
from retrieve_twitter_info import SListener
import time, tweepy, sys

app_token = 'XXXXXXXXXXXXXXX'
app_secret = 'XXXXXXXXXXXXXXX'
auth_token = 'XXXXXXXXXXXXXXX'
auth_secret = 'XXXXXXXXXXXXXXX'

twitter = Twython(
	app_key=app_token,
	app_secret=app_secret,
	oauth_token=auth_token,
	oauth_token_secret=auth_secret)
auth = tweepy.OAuthHandler(app_token, app_secret)
auth.set_access_token(auth_token, auth_secret)
api = tweepy.API(auth)

slistener = SListener()
myStream = tweepy.Stream(auth = api.auth, listener=SListener())
myStream.filter(track=['trump'])



#retrieveaccountinfo(twitter, ['katyperry', 'darry'])

#def checktweetdifference(twitter, users_to_retrieve):

#print(fromnametoid(twitter, ['katyperry']))

#checktweetdifference(twitter, ['katyperry'])

