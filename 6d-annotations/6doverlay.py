import cv2
from cv2 import data
import pandas as pd

from os import listdir
from os.path import isfile, join

ANNOTATION_PATH = '6d-annotations/resources/annotations'
IMAGE_PATH = '6d-annotations/resources/images'

def read_annotations():
    cols = ['class', 'x0', 'y0', 'x1', 'y1', 'x2', 'y2',
        'x3', 'y3', 'x4', 'y4', 'x5', 'y5', 'x6', 'y6', 'x7', 'y7','x8', 'y8',
        'x-range', 'y-range']

    data = {}

    annotationFiles = [f for f in listdir(ANNOTATION_PATH) if isfile(join(ANNOTATION_PATH, f))]

    for annotationFile in annotationFiles:
        with open(ANNOTATION_PATH + '/' + annotationFile, 'r') as f:
            output = f.read().split()
            for i, o in enumerate(output):
                if not cols[i] in data:
                    data[cols[i]] = []
                data[cols[i]].append(float(o))
    
    df = pd.DataFrame.from_dict(data)
    return df

def read_image():
    imageFiles = [f for f in listdir(IMAGE_PATH) if isfile(join(IMAGE_PATH, f))]

    for image in imageFiles:
        img = cv2.imread(IMAGE_PATH + '/' + image)

        cv2.imshow('image', img)

        if cv2.waitKey(0) == ord('q'):
             break

if __name__ == "__main__":
    df = read_annotations()
    read_image()
    print(df)
    cv2.destroyAllWindows()