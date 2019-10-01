import json
import time

import requests


def get_monthly_data_for_topic(topic):
  url = f'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/{article}/monthly/2016010100/2019123100'
  r = requests.get(url)
  time.sleep(2)
  return r.json()


def get_articles_data_from_search_query(q):
  
  URL = "https://en.wikipedia.org/w/api.php"

  SEARCHPAGE = "biology"

  PARAMS = {
      'action':"query",
      'list':"search",
      'srsearch': q,
      'format':"json",
      'prop':'info',
      'inprop':'url'
  }

  r = requests.get(url=URL, params=PARAMS)
  search_data = r.json()['query']

  time.sleep(2)

  return search_data




def get_url_stem_from_pageid(pageid):

  URL = "https://en.wikipedia.org/w/api.php"

  PARAMS = {
      'action':"query",
      'prop':"info",
      'pageids': pageid,
      'inprop':'url',
      'format':'json'
  }

  r = requests.get(url=URL, params=PARAMS)
  data = r.json()


  stem = data['query']['pages'][str(pageid)]['canonicalurl'].split('/')[-1]

  time.sleep(2)

  return stem



def get_monthly_data_for_article(article,start='20180101',end='20181231'):

  print(f'pulling {article} data')

  url = f'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/{article}/monthly/{start}/{end}'
  r = requests.get(url)

  time.sleep(2)

  return r.json()['items']


def get_annual_views_for_article(article,year):
  start = f'{year}0101'
  end = f'{year}1231'
  month_data = get_monthly_data_for_article(article,start=start,end=end)
  views = 0
  for m in month_data:
    views += m['views']
  return views

def get_annual_views_for_query(query,year):
	pageid = get_articles_data_from_search_query(query)['search'][0]['pageid']
	article = get_url_stem_from_pageid(pageid)
	views = get_annual_views_for_article(article,year)
	return views


def get_url_from_search_term(query):
	pageid = get_articles_data_from_search_query(query)['search'][0]['pageid']
	article = get_url_stem_from_pageid(pageid)
	return article


def get_wordcount_for_first_entry_for_search_term(query):
	print(f'pulling first article wordcount for {query}')
	wordcount = get_articles_data_from_search_query(query)['search'][0]['wordcount']
	return wordcount


def get_list_of_disciplines_from_wikipedia():

    endpoint_url = "https://query.wikidata.org/sparql"
    
    query = '''
    SELECT ?item ?itemLabel
    WHERE
    {
      ?item wdt:P31/wdt:P279* wd:Q11862829.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    '''


    agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    
    r = requests.get(endpoint_url, params = {'format': 'json', 'query': query, 'agent':agent})
    data = r.json()

    return data
