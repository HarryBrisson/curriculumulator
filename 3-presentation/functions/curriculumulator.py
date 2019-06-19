import pandas as pd

def get_curriculumulator_data():

	df = pd.read_csv('static/data/summary.csv')
	data_string = df.to_json(orient='records')
	option_list = df.select_dtypes(exclude=['object']).columns

	data = {
		'data_string': data_string,
		'option_list': option_list,
		}

	return data
