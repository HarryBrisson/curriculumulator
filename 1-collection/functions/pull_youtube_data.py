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


def get_video_stats(video_id):

	stats = {}

	api_key = get_youtube_api_key()
	url = r"https://www.googleapis.com/youtube/v3/videos?part=statistics&id="+video_id+"&key="+api_key
	print("pulling stats for "+video_id)

	for trial in range(5):
		try:
			r = requests.get(url, timeout=5)
			d = json.loads(r.text)['items'][0]
			break
		except Exception as e:
			print(e)
			if trial < 2:
				print("trying again")
			else:
				print("moving on")
				d = {}

	try:
		stats['comments'] = d['statistics']['commentCount']
	except:
		stats['comments'] = ''

	try:
		stats['likes'] = d['statistics']['likeCount']
	except:
		stats['likes'] = ''

	try:
		stats['dislikes'] = d['statistics']['dislikeCount']
	except:
		stats['dislikes'] = ''

	try:
		stats['views'] = d['statistics']['viewCount']
	except:
		stats['views'] = ''

	# ideally want this to match the youtube datetime format for easy comparison
	stats['collection_datetime'] = datetime.datetime.utcnow()


	return stats


