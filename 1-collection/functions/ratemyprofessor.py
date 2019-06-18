import requests
from bs4 import BeautifulSoup

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
        'campus':{
            'name':campus_name,
            'id':campus_id
        },
        'dept':department_name,
        'name':professor_name,
        'scores':{
            'quality':quality,
            'retake':retake,
            'difficulty':difficulty,
        }
    }

    return data