import cv2
import json
import math
import pandas as pd

frameWidth = 640
frameHeight = 480

# cap = cv2.VideoCapture("resources/object_detect_test_vid.mp4")
cap = cv2.VideoCapture("resources/new-car/sample_toy_car.mp4")
cap.set(cv2.CAP_PROP_FPS, 20)

# df = pd.read_csv('resources/3d-annotation.csv')
df1 = pd.read_csv('resources/bb3d-new-car.csv')
df2 = pd.read_csv('resources/new-car/cvat-bb3d-annotation.csv')

df = pd.concat([df1,df2],axis=0).reset_index(drop=True)

df = df.fillna('-1')

out = cv2.VideoWriter('output/bb3d-new-car.mp4', -1, 20.0, (frameWidth, frameHeight))

def draw_face(img, p, colour):
    for i in range(len(p)):
        j = i + 1
        if i + 1 == len(p):
            j = 0
        cv2.line(img, (int(p[i][0]), int(p[i][1])), (int(p[j][0]), int(p[j][1])), colour, 5)
    return img

def draw_overlay(img, points, faces):
    colour = (255, 0, 0)
    for face in faces:
        img = draw_face(img, [points[face[0]], points[face[1]], points[face[2]], points[face[3]]], colour)
    return img

count = 0
while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.resize(img, (frameWidth, frameHeight))

    data = df.loc[df['count'] == count]

    if not data.empty:
        if data['points'].iloc[0] == '-1':
            points = []
            faces = []
        else:
            points = json.loads(data['points'].iloc[0])
            faces = json.loads(data['faces'].iloc[0])

            img = draw_overlay(img, points, faces)

    cv2.imshow("Result", img)

    out.write(img)

    if cv2.waitKey(1) == ord('q'):
        break
    count+=1

cap.release()
out.release()
cv2.destroyAllWindows()
