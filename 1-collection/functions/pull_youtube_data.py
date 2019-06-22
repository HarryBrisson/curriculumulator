import json
import time

import pandas as pd
import requests
def get_youtube_api_key():
	with open(r"authorizations/youtube-api-key.txt", 'r') as f:
		api_key=f.read().replace("\n","")
	return api_key

def get_videos_for_search_term(q):

	api_key = get_youtube_api_key()

	params = {
		'part':'snippet',
		'order':'viewCount',
		'q':q,
		'type':'video',
		'key':api_key,
	}

	uri = 'https://www.googleapis.com/youtube/v3/search'


	print("searching for vids relating to "+q)
	r = requests.get(uri,params=params)

	return r.json()


