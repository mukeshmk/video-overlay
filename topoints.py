import pandas as pd
import json

# df = pd.read_csv('resources/export-300frames.csv')
df1 = pd.read_csv('resources/export-2020-07-22T09_31_50.351Z.csv')
df2 = pd.read_csv('resources/export-2020-07-22T10_22_28.850Z.csv')

df = pd.concat([df1,df2],axis=0).reset_index(drop=True)

data = {}
data['count'] = []
data['points'] = []
for index, row in df.iterrows():
    data['count'].append(row['External ID'].replace('img-', '').replace('.jpg', ''))
    jsondump = json.loads(row['Label'])
    data['points'].append(json.dumps(jsondump['objects'][0]['line']))

new_df = pd.DataFrame.from_dict(data)

new_df.sort_values(by=['count'], inplace = True)
new_df.to_csv('resources/required-data.csv', index=False)
