import cv2
from cv2 import data
import pandas as pd

from os import listdir
from os.path import isfile, join

PATH = '6d-annotations/resources/annotations'

def read_annotations():
    cols = ['class', 'x0', 'y0', 'x1', 'y1', 'x2', 'y2',
        'x3', 'y3', 'x4', 'y4', 'x5', 'y5', 'x6', 'y6', 'x7', 'y7','x8', 'y8',
        'x-range', 'y-range']

    data = {}

    annotationFiles = [f for f in listdir(PATH) if isfile(join(PATH, f))]

    for annotationFile in annotationFiles:
        with open(PATH + '/' + annotationFile, 'r') as f:
            output = f.read().split()
            for i, o in enumerate(output):
                if not cols[i] in data:
                    data[cols[i]] = []
                data[cols[i]].append(float(o))
    
    df = pd.DataFrame.from_dict(data)
    return df

if __name__ == "__main__":
    df = read_annotations()
    print(df)