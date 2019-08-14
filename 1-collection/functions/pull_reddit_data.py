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

def main():
    data = identify_homeworkhelp_posts()
    df = pd.DataFrame(data)
    print(df)
    return df


if __name__ == '__main__':
	main()