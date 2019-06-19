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

