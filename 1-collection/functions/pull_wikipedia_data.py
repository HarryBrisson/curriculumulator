import json

import requests


def get_monthly_data_for_topic(topic):
  url = f'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/{article}/monthly/2016010100/2019123100'
  r = requests.get(url)
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

  return stem



def get_monthly_data_for_article(article,start='20180101',end='20181231'):

  url = f'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/{article}/monthly/{start}/{end}'
  r = requests.get(url)
  return r.json()['items']

