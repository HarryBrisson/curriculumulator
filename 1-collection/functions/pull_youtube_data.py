import json
import time

import pandas as pd
import requests
def get_youtube_api_key():
	with open(r"authorizations/youtube-api-key.txt", 'r') as f:
		api_key=f.read().replace("\n","")
	return api_key

