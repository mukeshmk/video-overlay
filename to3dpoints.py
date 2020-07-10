import json
import pandas as pd

data = {}
data['count'] = []
data['faces'] = []
data['points'] = []


for i in range(300):
    f = open('resources/cars/frames/ann/img-'+ str(i) +'.jpg.json') 
    
    obj = json.load(f)
    data['count'].append(i)
    if(len(obj['objects']) == 0):
        data['faces'].append('')
        data['points'].append('')
    else:
        data['faces'].append(json.dumps(obj['objects'][0]['faces']))
        data['points'].append(json.dumps(obj['objects'][0]['points']))
    
    f.close()

df = pd.DataFrame.from_dict(data)

df.to_csv('resources/3d-annotation.csv')