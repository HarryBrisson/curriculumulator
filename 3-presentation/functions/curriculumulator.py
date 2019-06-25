
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


def rgb_to_hex(RGB):
    RGB = [int(x) for x in RGB]
    RGB_strings = ["0{0:x}".format(v) if v < 16 else "{0:x}".format(v) for v in RGB]
    hex_color = "#"+"".join(RGB_strings)
    return hex_color


def pctl_to_pctl_color(pctl):
    try:
        pctl_color = [int((1-pctl)*255),int(pctl*255),0]
        pctl_hex = rgb_to_hex(pctl_color)
    except:
        pctl_hex = None
    return pctl_hex


def index_to_index_color(i):
    try:
        
        if i<25:
            r = 255
            g = 0
            b = 0
        elif i>400:
            r = 0
            g = 255
            b = 0
        elif i < 100:
            r = 255
            g = int((i-25)/75*255)
            b = int((i-25)/75*255)
        elif i > 100:
            r = int((300-(i-100))/300*255)
            g = 255
            b = int((300-(i-100))/300*255)
            
        index_color = [r,g,b]
        index_hex = rgb_to_hex(index_color)
        
    except:
        index_hex = None
        
    return index_hex



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

    df['pctl_color'] = df['percentile'].apply(lambda x: pctl_to_pctl_color(x))
    df['index_color'] = df['index'].apply(lambda x: index_to_index_color(x))

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


