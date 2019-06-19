
import os

import pandas as pd

from functions.pull_ratemyprofessor_data import *
from functions.pull_wikipedia_data import *
from functions.pull_twitter_data import *


def create_core_data():

	with open('data/departments.txt','r') as f:
	    data = f.read().split('\n')
	    
	df = pd.DataFrame(data).rename(columns={0:'dept'})


	df['tweets_per_hour'] = df['dept'].apply(lambda x: get_tweets_per_hour_estimate(x))
	df['wikipedia_url'] = df['dept'].apply(lambda x: get_url_from_search_term(x))
	df['2018_wikipedia_views'] = df['wikipedia_url'].apply(lambda x: get_annual_views_for_article(x,2018))
	df['wikipedia_wordcount'] = df['dept'].apply(lambda x: get_wordcount_for_first_entry_for_search_term(x))

	df.to_csv('data/behaviors.csv')


if __name__ == '__main__':
	create_core_data()
