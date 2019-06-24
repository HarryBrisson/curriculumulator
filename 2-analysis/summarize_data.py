import os

import pandas as pd

def get_aggregated_dept_name(dept):

    dept_aggregator = {
        'Academic Development': 'Education',
        'Accounting & Finance': 'Accounting',
        'Adult Basic Education': 'Education',
        'Advertising Design': 'Advertising',
        'Analytics & Technology': 'Technology',
        'Anatomy & Physiology': 'Anatomy',
        'Animation': 'Media Arts & Animation',
        'Applied Business Statistics': 'Statistics',
        'Asian American Studies': 'Asian & Asian American Studies',
        'Asian Studies': 'Asian & Asian American Studies',
        'Athletic Training': 'Athletics & Physical Education',
        'Athletics': 'Athletics & Physical Education',
        'Atmospheric Sciences': 'Meteorology',
        'Behavioral & Social Sciences': 'Behavioral & Social Sciences',
        'Behavioral Sciences': 'Behavioral & Social Sciences',
        'Beverage Management': 'Food & Beverage Management',
        'Bible, Missions & Ministry': 'Biblical Ministry',
        'Bible/Christian Ministry': 'Biblical Ministry',
        'Biblical & Religious Studies': 'Biblical Studies',
        'Biblical Counseling': 'Biblical Studies',
        'Biblical Worldview': 'Biblical Studies',
        'Biomedical Engineering': 'Biomedical',
        'Business  Finance': 'Finance',
        'Business & Organizationl Ldshp': 'Management',
        'Business Management': 'Management',
        'Chemistry & Biochemistry': 'Biochemistry',
        'Chicano Studies': 'Hispanic & Chicano Studies',
        'Child & Family Studies': 'Family Studies / Family & Consumer Sciences',
        'Christian Ministries': 'Biblical Ministry',
        'Cinema': 'Film',
        'Classical Studies': 'Classics',
        'Comparative Studies in Literature & Culture': 'Comparative Literature',
        'Computer  Informational Tech.': 'Computer & Information Technology',
        'Computer & Information Technology & Engineering': 'Computer & Information Technology',
        'Computer & Informational Tech.': 'Computer & Information Technology',
        'Computer Animation': 'Media Arts & Animation''Animation',
        'Computer Applications': 'Computer Engineering',
        'Computer Information Tech.': 'Computer & Information Technology',
        'Computer Systems Technology': 'Computing & Technology',
        'Computer Technologies': 'Computing & Technology',
        'Consumer Family Science': 'Family Studies / Family & Consumer Sciences',
        'Contemporary Music Writing': 'Music',
        'Counseling  Educational Psych': 'Counseling',
        'Counseling Psychology': 'Counseling',
        'Counselor Education': 'Counseling',
        'Criminal Justice': 'Criminology & Criminal Justice',
        'Criminology': 'Criminology & Criminal Justice',
        'Criminology & Criminal Justice': 'Criminology & Criminal Justice',
        'Decision & Info Science': 'Decision & Info Science',
        'Decision Science': 'Decision & Info Science',
        'Dietetics': 'Nutrition',
        'Digital Arts': 'Digital Arts & Media',
        'Digital Media': 'Digital Arts & Media',
        'Digital Media Production': 'Digital Arts & Media',
        'Distance Learning': 'Education',
        'Dramatic Arts': 'Theater',
        'East Asian Studies': 'Asian & Asian American Studies',
        'Engineering  Technology': 'Engineering Technology',
        'Engineering Mathematics': 'Engineering',
        'Engineering Technology': 'Engineering',
        'English  Liberal Studies': 'English',
        'English & Liberal Studies': 'English',
        'English & Literature': 'English',
        'English & Reading': 'English',
        'English Language & Literature': 'English',
        'Entrepreneurship': 'Management & Entrepreneurship',
        'Environmental Sci & Eng': 'Environmental Science',
        'Evangelism': 'Biblical Ministry',
        'Exercise & Sport Science': 'Athletics & Physical Education',
        'Family & Child Sciences': 'Family Studies / Family & Consumer Sciences',
        'Family & Consumer Science': 'Family Studies / Family & Consumer Sciences',
        'Family & Consumer Sciences': 'Family Studies / Family & Consumer Sciences',
        'Family Life': 'Family Studies / Family & Consumer Sciences',
        'Family Social Science': 'Family Studies / Family & Consumer Sciences',
        'Family Studies': 'Family Studies / Family & Consumer Sciences',
        'Fashion': 'Fashion & Fashion Business Management',
        'Fashion Business Management': 'Fashion & Fashion Business Management',
        'Film Studies': 'Film',
        'Finance & Business Law': 'Finance',
        'Foods & Nutrition': 'Nutrition',
        'Foreign Languages': 'Foreign Languages & Literature',
        'Foreign Languages  Literature': 'Foreign Languages & Literature',
        'Foundations of Am. Culture/Classics': 'American Studies',
        'Gender Studies': "Women's Studies",
        'General Education': 'General Studies',
        'Global Studies': 'International Studies',
        'Harmony': 'Music',
        'Health Administration': 'Health Care Administration',
        'Hispanic Studies': 'Hispanic & Chicano Studies',
        'Home & Family Studies': 'Family Studies / Family & Consumer Sciences',
        'Hotel & Restaurant Management': 'Hospitality',
        'Jewish History': 'Judaic Studies',
        'Journalism & Media Studies': 'Media Studies',
        'Law & Society': 'Legal Studies',
        'Liberal Arts  Sciences': 'Liberal Arts & Sciences',
        'Management & Entrepreneurship': 'Entrepreneurship',
        'Management Sciences': 'Management',
        'Managerial Science': 'Management',
        'Mass Communications': 'Communications',
        'Math & Statisitics': 'Mathematics & Statistics',
        'Media, Journalism & Film': 'Media Studies',
        'Medieval Studies': 'History',
        'Molecular Biosciences': 'Molecular Biology',
        'Molecular/Cellular Biology': 'Molecular Biology',
        'Natural Science': 'Natural Sciences',
        'Neurological Sciences': 'Neuroscience',
        'Nutrition  Foods': 'Nutrition',
        'Nutrition & Exercise Sci': 'Nutrition',
        'Nutrition & Foods': 'Nutrition',
        'Operations  Mgmt Info Systems': 'Operations Management',
        'Operations & Mgmt Info Systems': 'Operations Management',
        'Painting': 'Visual Arts',
        'Pharmacology': 'Pharmaceutical Sciences',
        'Pharmacy': 'Pharmaceutical Sciences',
        'Philosophy & History': 'Humanities',
        'Philosophy & Religion': 'Humanities',
        'Photography': 'Visual Arts',
        'Physical Ed': 'Athletics & Physical Education',
        'Physical Education': 'Athletics & Physical Education',
        'Physics & Astronomy': 'Astronomy',
        'Physics & Planetary Sciences': 'Astronomy',
        'Poli-Science & Crim. Justice': 'Criminology & Criminal Justice',
        'Political Science & Law': 'Legal Studies',
        'Political Science & Public Administration': 'Public Policy & Administration',
        'Public Administration': 'Public Policy & Administration',
        'Public Policy': 'Public Policy & Administration',
        'Radiography': 'Radiological Sciences',
        'Rehabilitation Counseling': 'Counseling',
        'Russian': 'Slavic Languages & Literatures',
        'Science & Family': 'Family Studies / Family & Consumer Sciences',
        'Social & Behavioral Sciences': 'Social Science',
        'Social Sciences': 'Social Science',
        'Sports': 'Athletics & Physical Education',
        'Student Development': 'Education',
        'Student Success': 'Education',
        'Studio Art': 'Visual Arts',
        'Systematic Theology': 'Theology',
        'TV & Radio': 'Communications',
        'Teacher Education': 'Education',
        'Telecommunications & Bus. Ed': 'Telecommunications',
        'Textiles & Clothing': 'Fashion & Fashion Business Management',
        'Theater & Rhetoric': 'Theater',
        'Transportation amp Logistics': 'Transportation & Logistics',
        'Web Design & Interactive Media': 'Web Design',
        'Women': "Women's Studies",
        'Youth Ministry': 'Biblical Ministry',
        'Zoology / Chemistry & Biochem.': 'Zoology'
    }

    try:
        new_dept = dept_aggregator[dept]
    except:
        new_dept = dept

    return dept


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

    # aggregate by new dept names here

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

def aggregate_subject_datasets(min_reviews_per_professor=5, min_professors_per_dept=5):
    summary = summarize_rmp_data(
        min_reviews_per_professor=min_reviews_per_professor, min_professors_per_dept=min_professors_per_dept
        )
    store_list_of_departments(summary)
    behaviors = pd.read_csv('../1-collection/data/behaviors.csv').set_index('dept')
    behaviors = behaviors.drop('Unnamed: 0',axis=1)
    summary = summary.join(behaviors)
    return summary

def clean_summary_data(summary):
    summary.columns = [c.replace("'",'') for c in summary.columns]
    summary.to_csv('../3-presentation/static/data/summary.csv')

if __name__ == "__main__":
    summary = aggregate_subject_datasets()
    clean_summary_data(summary)