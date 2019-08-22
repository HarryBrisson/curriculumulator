import os

import pandas as pd

def import_all_reddit_jsons():
	df = pd.DataFrame()
	file_dir = '../1-collection/data/reddit'
	files = ['/'.join([file_dir,f]) for f in os.listdir(file_dir) if 'json' in f]
	for f in files:
		print(f'appending {f}')
		df = df.append(pd.read_json(f),ignore_index=True)
	return df

def create_aggregated_reddit_json_file():
	df = import_all_reddit_jsons()
	df.to_json('data/reddit.json',orient='records')

def get_subjects():
	subjects = list(pd.read_csv('../3-presentation/static/data/summary.csv')['dept'])
	return subjects

def calculate_subject_scores(subjects):
	df = pd.read_json('data/reddit.json')
	for s in subjects:
		df[s] = df['title'].apply(lambda x: s.lower() in x.lower())
	return df

def create_subject_summary_df(df,subjects):
	summary = []
	for s in subjects:
		row = {}
		row['subject'] = s
		row['Homework Help Posts'] = sum(df[s])
		row['Homework Help Comments'] = sum(df[s]*df['num_comments'])
		row['Homework Help Score'] = sum(df[s]*df['score'])
		try:
			row['Homework Help Comments Per Post'] = row['Homework Help Comments']/row['Homework Help Posts']
		except:
			row['Homework Help Comments Per Post'] = 0
		summary.append(row)
	sdf = pd.DataFrame(summary)
	return sdf
		

def create_subject_homework_df():
	subjects = get_subjects()
	df = calculate_subject_scores(subjects)
	sdf = create_subject_summary_df(df,subjects)
	return sdf


def main():
	df = import_all_reddit_jsons()
	df.to_json('data/reddit.json',orient='records')
	subjects = get_subjects()
	calculate_subject_scores(subjects)

if __name__ == '__main__':
	main()