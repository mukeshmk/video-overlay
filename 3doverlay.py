import cv2
import json
import math
import pandas as pd

frameWidth = 640
frameHeight = 480

cap = cv2.VideoCapture("resources/object_detect_test_vid.mp4")
cap.set(cv2.CAP_PROP_FPS, 20)

df = pd.read_csv('resources/3d-annotation.csv')
df = df.fillna('-1')

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

count = 0
while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.resize(img, (frameWidth, frameHeight))

    data = df.loc[df['count'] == count]

    if data['points'].iloc[0] == '-1':
        points = []
        faces = []
    else:
        points = json.loads(data['points'].iloc[0])
        faces = json.loads(data['faces'].iloc[0])

        img = draw_overlay(img, points, faces)

    cv2.imshow("Result", img)

    if cv2.waitKey(1) == ord('q') or count + 2 > 300:
        break
    count+=1

cap.release()
cv2.destroyAllWindows()
