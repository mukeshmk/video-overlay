from xml.dom import minidom
import pandas as pd
import json

no_of_files = 5

xmldoc = []
imagenamelist = []
itemlist = []

for i in range(no_of_files):
    xmldoc.append(minidom.parse('resources/new-car/bb3d-annotations/annotations-0' + str(i+1) + '.xml'))
    imagenamelist.append(xmldoc[i].getElementsByTagName('image'))
    itemlist.append(xmldoc[i].getElementsByTagName('cuboid'))

df = pd.DataFrame(columns=['count', 'faces', 'points'])

def format_data(data, itemlist, imagenamelist):
    for item, image in zip(itemlist, imagenamelist):
        count = int(image.attributes['name'].value.replace('1200-1416/','').replace('img-', '').replace('images', '').replace('.jpg', ''))

        points = [
            [int(float(item.attributes['xbr2'].value)), int(float(item.attributes['ybr2'].value))], #0
            [int(float(item.attributes['xtr2'].value)), int(float(item.attributes['ytr2'].value))], #1
            [int(float(item.attributes['xbl2'].value)), int(float(item.attributes['ybl2'].value))], #2
            [int(float(item.attributes['xtl2'].value)), int(float(item.attributes['ytl2'].value))], #3
            [int(float(item.attributes['xbr1'].value)), int(float(item.attributes['ybr1'].value))], #4
            [int(float(item.attributes['xtr1'].value)), int(float(item.attributes['ytr1'].value))], #5
            [int(float(item.attributes['xbl1'].value)), int(float(item.attributes['ybl1'].value))], #6
            [int(float(item.attributes['xtl1'].value)), int(float(item.attributes['ytl1'].value))]  #7
            ]

        data['count'].append(count)
        data['faces'].append(json.dumps(faces))
        data['points'].append(json.dumps(points))

    return data

if not len(imagenamelist) == len(itemlist):
    print('length miss match check XML file!')
else:
    faces = [[0, 1, 3, 2], [0, 1, 7, 6], [2, 3, 5, 4], [4, 5, 7, 6]]

    data = {}
    data['count'] = []
    data['faces'] = []
    data['points'] = []
        
    for item, imagename in zip(itemlist, imagenamelist):
        data = format_data(data, item, imagename)
        
    df = df.append(pd.DataFrame.from_dict(data), ignore_index=True)

print(df.shape)
df.to_csv('resources/new-car/cvat-bb3d-annotation.csv', index=False)
