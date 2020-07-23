from xml.dom import minidom
import pandas as pd
import json

no_of_files = 4

xmldoc = []
imagenamelist = []
itemlist = []

for i in range(no_of_files):
    xmldoc.append(minidom.parse('resources/new-car/cvat-annotations/annotations-0' + str(i+1) + '.xml'))
    imagenamelist.append(xmldoc[i].getElementsByTagName('image'))
    itemlist.append(xmldoc[i].getElementsByTagName('cuboid'))

df = pd.DataFrame(columns=['count', 'faces', 'points'])

def format_data(data, itemlist, imagenamelist):
    for item, image in zip(itemlist, imagenamelist):
        count = int(image.attributes['name'].value.replace('img-', '').replace('images', '').replace('.jpg', ''))

        points = [[int(float(item.attributes['xbr2'].value)), int(float(item.attributes['ybr2'].value))], 
            [int(float(item.attributes['xtr2'].value)), int(float(item.attributes['ytr2'].value))], 
            [int(float(item.attributes['xbl2'].value)), int(float(item.attributes['ybl2'].value))], 
            [int(float(item.attributes['xtl2'].value)), int(float(item.attributes['ytl2'].value))], 
            [int(float(item.attributes['xbr1'].value)), int(float(item.attributes['ybr1'].value))], 
            [int(float(item.attributes['xtr1'].value)), int(float(item.attributes['ytr1'].value))], 
            [int(float(item.attributes['xbl1'].value)), int(float(item.attributes['ybl1'].value))], 
            [int(float(item.attributes['xtl1'].value)), int(float(item.attributes['ytl1'].value))]]

        data['count'].append(count)
        data['faces'].append(json.dumps(faces))
        data['points'].append(json.dumps(points))

    return data

if not len(imagenamelist) == len(itemlist):
    print('length miss match check XML file!')
else:
    faces = [[0, 1, 2, 3], [0, 4, 5, 1], [1, 5, 6, 2]]

    data = {}
    data['count'] = []
    data['faces'] = []
    data['points'] = []
        
    for item, imagename in zip(itemlist, imagenamelist):
        data = format_data(data, item, imagename)
        
    df = df.append(pd.DataFrame.from_dict(data), ignore_index=True)

print(df.shape)
df.to_csv('resources/new-car/cvat-bb3d-annotation.csv', index=False)
