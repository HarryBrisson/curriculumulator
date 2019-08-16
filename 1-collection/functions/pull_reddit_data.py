import time
from calendar import timegm
import datetime

import requests
from bs4 import BeautifulSoup
import pandas as pd
import praw


def get_client_secret():
    with open(r"authorizations/reddit-secret.txt", 'r') as f:
        api_key=f.read().replace("\n","")
    return api_key

def identify_homeworkhelp_posts():
    reddit = praw.Reddit(client_id='am_DaL0ACH9R7Q',
                     client_secret=get_client_secret(),
                     user_agent='ubuntu:curriculumular:v0.0.1 (by /u/NotSorryImSorry)')

    submissions = reddit.subreddit('homeworkhelp').new(limit=1000)

    data = []

    for s in submissions:
        row = {}
        row['title'] = s.title
        row['comments'] = s.num_comments 
        row['tags'] = s.link_flair_text
        row['time'] = s.created_utc
        data = data + [row] 
      
    return data

def get_subreddit_posts_for_date(subreddit,date):
    utc_time = time.strptime(date, "%Y-%m-%d")
    d1 = timegm(utc_time)
    d2 = d1 + (24 * 60 * 60)

    url = f"https://api.pushshift.io/reddit/search/submission/?subreddit=homeworkhelp&size=500&after={d1}&before={d2}"
    print(url)
    r = requests.get(url)
    data = r.json()['data']
    return data

def generate_list_of_days(days_back_to_go):
    base = datetime.datetime.today()
    date_list = [base - datetime.timedelta(days=x) for x in range(days_back_to_go)]
    return date_list

def main():

    dates = generate_list_of_days(365)

    for d in dates:
        date = d.strftime('%Y-%m-%d')
        data = get_subreddit_posts_for_date('homeworkhelp',date)
        df = pd.DataFrame(data)
        df.to_json(f'data/reddit/{date}.json', orient="records")
        time.sleep(3)


if __name__ == '__main__':
	main()