import requests
from bs4 import BeautifulSoup
import pandas as pd
import praw


def get_client_secret():
    with open(r"authorizations/reddit-secret.txt", 'r') as f:
        api_key=f.read().replace("\n","")
    return api_key


def main():
    return


if __name__ == '__main__':
	main()