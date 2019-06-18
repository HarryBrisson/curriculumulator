
import urllib
import time
import json


import requests
from bs4 import BeautifulSoup
import pandas as pd

from selenium import webdriver  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys


def remove_whitespace(s):
    s = s.strip()
    s = s.replace('\n','').replace('\t','').replace('\r','')
    s = " ".join(s.split())
    return s


def pull_data_for_professor(tid):


    url = 'https://www.ratemyprofessors.com/ShowRatings.jsp'
    params = {
        'tid':tid,
        'showMyProfs':'true'
    }
    
    r = requests.get(url,params=params)
    soup = BeautifulSoup(r.text,'html.parser')

    professor_name = soup.find('h1',{'class':'profname'}).getText()
    professor_name = remove_whitespace(professor_name)

    rating_count = soup.find('div',{'class':'rating-count'}).getText().replace('Student Ratings',"")
    rating_count = remove_whitespace(rating_count)
    
    scores = soup.find_all('div',{'class':'grade'})
    quality = remove_whitespace(scores[0].getText())
    retake = remove_whitespace(scores[1].getText())
    difficulty = remove_whitespace(scores[2].getText())

    metadata_div = soup.find('div',{'class':'result-title'})

    campus_id = metadata_div.find('a',{'class':'school'})['href'].split('=')[-1]
    campus_name = metadata_div.find('a',{'class':'school'}).getText().replace(',','')

    department_name = metadata_div.getText().split('Professor in the ')[-1].split(' department')[0]

    tags = [t.getText().strip() for t in soup.find_all('span',{'class':'tag-box-choosetags'})]
    
    data = {
        'campus_name':campus_name,
        'campus_id':campus_id,
        'rating_count':rating_count,
        'dept':department_name,
        'name':professor_name,
        'quality':quality,
        'retake':retake,
        'difficulty':difficulty,
    }
    
    for t in tags:
        tag_name, tag_score = t.split('(')
        tag_name = "tag_"+tag_name.strip().replace('.','').replace('?','').replace(' ','').lower()
        tag_score = tag_score.replace(')','')
        data[tag_name] = tag_score

    return data


def get_tids_for_sid(sid):
    
    url_base = 'https://www.ratemyprofessors.com/search.jsp'
    
    params = {
        'queryoption':'TEACHER',
        'queryBy':'schoolDetails',
        'schoolID':sid
    }    
    
    url = f'{url_base}?{urllib.parse.urlencode(params)}'
    

    # set up options for headless browser
    options = Options()
    options.add_argument("--headless")  

    # get region url
    browser = webdriver.Chrome(options=options)
    browser.get(url)
    print('accessed {}'.format(url))
    time.sleep(3)

    results = browser.find_elements_by_class_name('result-list')[-1]

    possibly_professors = results.find_elements_by_xpath('//li')

    possibly_tids = [p.get_attribute('id') for p in possibly_professors]

    tids = [t.replace('my-professor-','') for t in possibly_tids if 'my-professor' in t]

    browser.quit()
    
    return tids


def get_data_for_tids(tids):
    data = []
    for tid in tids:
        print(f'pulling data for {tid}')
        try:
            data += [pull_data_for_professor(tid)]
        except Exception as e:
            print(e)
        time.sleep(5)
    return data


def store_data_for_sid(sid):
    tids = get_tids_for_sid(sid)
    data = get_data_for_tids(tids)
    with open(f'data/rate-my-professor/{sid}.json', 'w') as f:
        json.dump(data, f)


def get_dataframe_for_downloaded_sid(sid):
    with open(f'data/rate-my-professor/{sid}.json', 'r') as f:
        data = json.load(f) 
    return pd.DataFrame(data)

def delete_downloaded_sid_json(sid):
	os.remove(f'data/rate-my-professor/{sid}.json')


def combine_json_files(start,end):
    filename = f'{start}-{end-1}.csv'
    df = pd.DataFrame()
    for i in range(start,end):
        temp_df = get_dataframe_for_downloaded_sid(i)
        df = df.append(temp_df,ignore_index=True)
    df.to_csv(f'data/rate-my-professor/{filename}')
    for i in range(start,end):
        delete_dataframe_for_downloaded_sid(i)

