import pandas as pd
import json

df = pd.read_csv('export.csv')

data = {}
data['count'] = []
data['points'] = []
for index, row in df.iterrows():
    data['count'].append(row['External ID'].replace('img-', '').replace('.jpg', ''))
    jsondump = json.loads(row['Label'])
    data['points'].append(jsondump['objects'][0]['line'])

new_df = pd.DataFrame.from_dict(data)

new_df.sort_values(by=['count'], inplace = True)
new_df.to_csv('required-data.csv', index=False)
