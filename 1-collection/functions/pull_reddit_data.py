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
    print(reddit)

def main():
    return


if __name__ == '__main__':
	main()