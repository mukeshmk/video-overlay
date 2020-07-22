import json
import pandas as pd

data = {}
data['count'] = []
data['faces'] = []
data['points'] = []

# count_range = range(300)
count_range = list(range(50, 100)) + list(range(101, 161))

for i in count_range:
    # f = open('resources/cars/frames/ann/img-'+ str(i) +'.jpg.json') 
    f = open('resources/new-car/bb3d-new-car/img-'+ str(i) +'.json') 
    
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

df.to_csv('resources/bb3d-new-car.csv', index=False)