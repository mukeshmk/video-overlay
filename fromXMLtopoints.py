from xml.dom import minidom
import pandas as pd
import json

no_of_files = 1

xmldoc = []
imagenamelist = []
itemlist = []

for i in range(no_of_files):
    xmldoc.append(minidom.parse('resources/new-car/polyline-annotatioins/annotations-0' + str(i+1) + '.xml'))
    imagenamelist.append(xmldoc[i].getElementsByTagName('image'))
    itemlist.append(xmldoc[i].getElementsByTagName('polyline'))

df = pd.DataFrame(columns=['count', 'points'])

def format_data(data, itemlist, imagenamelist):
    for item, image in zip(itemlist, imagenamelist):
        count = int(image.attributes['name'].value.replace('img-', '').replace('images', '').replace('.jpg', ''))

        point_data = []
        for point in item.attributes['points'].value.split(';'):
            points = {}
            points['x'] = float(point.split(',')[0])
            points['y'] = float(point.split(',')[1])
            point_data.append(points)

        data['count'].append(count)
        data['points'].append(json.dumps(point_data))

    return data

if not len(imagenamelist) == len(itemlist):
    print('length miss match check XML file!')
else:

    data = {}
    data['count'] = []
    data['points'] = []
        
    for item, imagename in zip(itemlist, imagenamelist):
        data = format_data(data, item, imagename)
        
    df = df.append(pd.DataFrame.from_dict(data), ignore_index=True)

print(df.shape)
df.to_csv('resources/new-car/cvat-polyline-annotation.csv', index=False)
