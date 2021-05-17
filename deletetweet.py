import tweepy
import json
import datetime

with open("settings.json") as f:
    settings = json.load(f)

# telegram authentication goes here
token = settings["telegramToken"]
channel_id = settings["channelId"]
# Twitter authentication goes here
consumer_key = settings["consumerKey"]
consumer_secret = settings["consumerSecret"]
access_token = settings["twitterAccessToken"]
access_token_secret = settings["accessTokenSecret"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
username ='YOUR_TWITTER_USER_NAME HERE'
MAX_TWEETS = 2000


for tweet in tweepy.Cursor(api.search, q='from:'+ username +' #getvaccinated', rpp=100).items(MAX_TWEETS):
    
    if not tweet.created_at.date() == datetime.datetime.now().date():
        print("deleting ->"+ str(tweet.id))
        try:
            api.destroy_status(tweet.id)
        except tweepy.TweepError as e:
            print("Tweepy Error: {}".format(e))
    
print('all bot generated tweets till yesterday has been deleted ')
    