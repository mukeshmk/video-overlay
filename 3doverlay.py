import cv2
import json
import math
import pandas as pd

frameWidth = 640
frameHeight = 480

df = pd.read_csv('resources/3d-annotation.csv')

def draw_face(img, p):
    for i in range(len(p)):
        j = i + 1
        if i + 1 == len(p):
            j = 0
        cv2.line(img, (int(p[i][0]), int(p[i][1])), (int(p[j][0]), int(p[j][1])), (255, 0, 0), 5)
    return img

def draw_overlay(img, points, faces):
    for face in faces:
        img = draw_face(img, [points[face[0]], points[face[1]], points[face[2]], points[face[3]]])
    return img

img = cv2.imread('img-10.jpg')
img = cv2.resize(img, (frameWidth, frameHeight))

if math.isnan(df['points']):
    points = []
    faces = []
else:
    points = json.loads(df['points'].iloc[0])
    faces = json.loads(df['faces'].iloc[0])

    img = draw_overlay(img, points, faces)

cv2.imshow("Result", img)

cv2.waitKey(0)
cv2.destroyAllWindows()
