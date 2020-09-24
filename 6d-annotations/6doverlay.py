import cv2
from cv2 import data
import pandas as pd

from os import listdir
from os.path import isfile, join

ANNOTATION_PATH = '6d-annotations/resources/annotations'
IMAGE_PATH = '6d-annotations/resources/images'
SAVE_PATH = '6d-annotations/output'
COLOURS = [
    (0,0,0),
 	(255,255,255),
 	(255,0,0),
 	(0,255,0),
 	(0,0,255),
 	(255,255,0),
 	(0,255,255),
 	(255,0,255),
 	(192,192,192),
 	(128,128,128),
 	(128,0,0),
 	(128,128,0),
 	(0,128,0),
 	(128,0,128),
 	(0,128,128),
 	(0,0,128)
]

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
                if 'x' in cols[i]:
                    data[cols[i]].append(int(float(o)*640))
                elif 'y' in cols[i]:
                    data[cols[i]].append(int(float(o)*480))
                else:
                    data[cols[i]].append(int(o))
    
    df = pd.DataFrame.from_dict(data)
    return df

def draw_overlay(img, points):
    X = 'x'
    Y = 'y'
    LEN = 9

    prev_point = None
    for i in range(LEN):
        if i == 0:
            cv2.circle(img, (points.iloc[0][X+str(i)], points.iloc[0][Y+str(i)]), 3, (0, 255, 0), -1)
        else:
            if prev_point == None:
                prev_point = [points.iloc[0][X+str(i)], points.iloc[0][Y+str(i)]]
            cv2.line(img, (int(prev_point[0]), int(prev_point[1])), (points.iloc[0][X+str(i)], points.iloc[0][Y+str(i)]), COLOURS[i], 5)
            prev_point = [points.iloc[0][X+str(i)], points.iloc[0][Y+str(i)]]
    return img

def draw_points(img, points, img_name):
    X = 'x'
    Y = 'y'
    LEN = 9

    for j in range(LEN):
        for i in range(j):
            img = cv2.circle(img, (points.iloc[0][X+str(i)], points.iloc[0][Y+str(i)]), 3, COLOURS[i], -1)
        cv2.imwrite(SAVE_PATH + '/' + str(j) + '-' +img_name, img)
    return img

def read_image(df):
    imageFiles = [f for f in listdir(IMAGE_PATH) if isfile(join(IMAGE_PATH, f))]

    for i, image in enumerate(imageFiles):
        img = cv2.imread(IMAGE_PATH + '/' + image)
        #img = draw_points(img, df.iloc[[i]], image)
        img = draw_overlay(img, df.iloc[[i]])
        cv2.imshow('image', img)
        cv2.imwrite(SAVE_PATH + '/' + image, img)

        if cv2.waitKey(0) == ord('q'):
             break

if __name__ == "__main__":
    df = read_annotations()
    read_image(df)
    cv2.destroyAllWindows()
