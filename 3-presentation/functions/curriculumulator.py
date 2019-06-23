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


def get_scorecard_data(subject):
    
    df = pd.read_csv('static/data/summary.csv')

    pctls = pd.DataFrame()
    indices = pd.DataFrame()

    for c in df.columns:
        try:
            pctls[c] = df[c].rank(pct=True)
            indices[c] = df[c]/(df[c].mean())*100
        except:
            pctls[c] = df[c]
            indices[c] = df[c]

    pctls = pctls[pctls['dept']==subject].transpose()
    indices = indices[indices['dept']==subject].transpose()
    df = df[df['dept']==subject].transpose()


    pctls = pctls.rename(columns={df.columns[0]:'percentile'})
    indices = indices.rename(columns={df.columns[0]:'index'})
    df = df.rename(columns={df.columns[0]:'score'})


    df = df.join(pctls)
    df = df.join(indices)

    return df

