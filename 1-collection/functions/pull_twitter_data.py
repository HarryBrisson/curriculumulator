import json
import time
import datetime

import requests
from requests_oauthlib import OAuth1
import pandas as pd

def get_twitter_auth():

	with open(r"authorizations/twitter_credentials.json", 'r') as f:
		cred=json.loads(f.read())

	auth = OAuth1(
		cred['api-key'],
		cred['api-secret'],
		cred['access-token'],
		cred['access-token-secret']
	)

	return auth

def get_recent_tweets(q):
	url = 'https://api.twitter.com/1.1/search/tweets.json'
	params = {
		'q':q,
		'result_type':'recent',
		'count':100
	}
	auth = get_twitter_auth()
	r = requests.get(url, params=params, auth=auth)
	time.sleep(5)
	return r.json()

def get_df_of_recent_tweets(q):

	tweets = get_recent_tweets(q)

	tweet_data = pd.DataFrame()

	for status in tweets['statuses']:
	    tweet = {}
	    tweet['text'] = status['text']
	    tweet['time'] = status['created_at']
	    tweet['user'] = status['user']['screen_name']
	    tweet['img'] = status['user']["profile_image_url"]
	    tweet['followers'] = status['user']["followers_count"]
	    tweet['favorites'] = status['favorite_count']
	    tweet['retweet'] = status['retweet_count']
	    tweet_data = tweet_data.append(tweet,ignore_index=True)
	    
	return tweet_data

def get_tweets_per_hour_estimate(q):
    data = get_recent_tweets(q)
    first_post = data['statuses'][0]['created_at']
    first_post = datetime.datetime.strptime(first_post,'%a %b %d %H:%M:%S +0000 %Y')
    last_post = data['statuses'][-1]['created_at']
    last_post = datetime.datetime.strptime(last_post,'%a %b %d %H:%M:%S +0000 %Y')
    tph = 100/((first_post - last_post).seconds/60/60)
    return int(tph)