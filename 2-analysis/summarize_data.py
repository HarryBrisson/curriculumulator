import os

import pandas as pd

def summarize_rmp_data(min_reviews_per_professor=5, min_professors_per_dept=5):

    rmp_files_path = '../1-collection/data/rate-my-professor'
    csvs = ['/'.join([rmp_files_path,f]) for f in os.listdir('../1-collection/data/rate-my-professor') if f[-4:]=='.csv']

    df = pd.DataFrame()
    for csv in csvs:
        df = df.append(pd.read_csv(csv),ignore_index=True)
    df = df.drop_duplicates(['campus_name','name'])
    df = df.drop('Unnamed: 0',axis=1)
    
    df = df[df['rating_count']>=min_reviews_per_professor]
    
    tag_columns = [c for c in df.columns if c[:3]=='tag']
    df[tag_columns] = df[tag_columns].fillna(0)

    for c in tag_columns:
        df[c] = df[c]/df['rating_count']
    
    summary = df[['dept','name']].groupby('dept').count().rename(columns={'name':'professors'})
    summary = summary.join(df[['dept','rating_count']].groupby('dept').sum())
    summary = summary.join(df[['dept','difficulty','quality','retake']+tag_columns].groupby('dept').mean())
    
    summary = summary[summary['professors']>=min_professors_per_dept]
    
    return summary


def store_list_of_departments(summary):
    dept_text = '\n'.join(list(summary.index))
    with open(f'../1-collection/data/departments.txt', 'w') as f:
        f.write(dept_text)

def main():
    summary = summarize_rmp_data()
    store_list_of_departments(summary)
    behaviors = pd.read_csv('../1-collection/data/behaviors.csv').set_index('dept')
    behaviors = behaviors.drop('0: Untitled',axis=1)
    summary = summary.join(behaviors)
    summary.columns = [c.replace("'",'') for c in summary.columns]
    summary.to_csv('../3-presentation/static/data/summary.csv')

if __name__ == "__main__":
    main()