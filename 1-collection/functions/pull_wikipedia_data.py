import json

import requests


def get_monthly_data_for_topic(topic):
  url = f'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/{article}/monthly/2016010100/2019123100'
  r = requests.get(url)
  return r.json()