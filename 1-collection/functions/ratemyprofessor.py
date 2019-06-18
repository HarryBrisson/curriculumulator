import requests
from bs4 import BeautifulSoup

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

    rating_count = soup.find('div',{'class':'rating-count'}).getText().replace('Student Ratings')
    rating_count = remove_whitespace(rating_count)
    
    scores = soup.find_all('div',{'class':'grade'})
    quality = remove_whitespace(scores[0].getText())
    retake = remove_whitespace(scores[1].getText())
    difficulty = remove_whitespace(scores[2].getText())

    metadata_div = soup.find('div',{'class':'result-title'})

    campus_id = metadata_div.find('a',{'class':'school'})['href'].split('=')[-1]
    campus_name = metadata_div.find('a',{'class':'school'}).getText()

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