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
        	if c == 'dept':
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

    df = df.reset_index()\
        .rename(columns={'level_0':'metric'})

    df.loc[df['metric'].str.contains('#'),'format'] = "{:.0f}"
    df.loc[df['metric'].str.contains('%'),'format'] = "{:.1%}"
    df.loc[df['metric'].str.contains('Score'),'format'] = "{:.2f}"

    return df



def prep_scorecard_df_as_dict(df):
    data = df.to_dict(orient='records')[1:]
    for d in data:
        try:
            d['score'] = d['format'].format(d['score'])
        except Exception as e:
            print(e)
        if d['metric'] == 'Wikipedia Url':
            d['score'] = f'en.wikipedia.org/wiki/{d["score"]}'
    return data


