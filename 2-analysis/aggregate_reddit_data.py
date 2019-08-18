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


def main():
	df = import_all_reddit_jsons()
	df.to_json('data/reddit.json',orient='records')

if __name__ == '__main__':
	main()