import cv2
import numpy as np
import json
import pandas as pd

frameWidth = 640
frameHeight = 480

# cap = cv2.VideoCapture("resources/object_detect_test_vid.mp4")
# link to the video: https://arlive.us/hackathon-2020/sample_toy_car.mp4
cap = cv2.VideoCapture("resources/new-car/sample_toy_car.mp4")

cap.set(cv2.CAP_PROP_FPS, 20)

# df = pd.read_csv('resources/required-data.csv')
df1 = pd.read_csv('resources/new-car/new-car.csv')
df2 = pd.read_csv('resources/new-car/cvat-polyline-annotation.csv')

df = pd.concat([df1,df2],axis=0).reset_index(drop=True)

# out = cv2.VideoWriter('output/output.mp4', -1, 20.0, (frameWidth, frameHeight))
out = cv2.VideoWriter('output/output-polyline-new-car.mp4', -1, 20.0, (frameWidth, frameHeight))

def draw_overlay(points):
    prev_point = None
    for point in points:
        if prev_point == None:
            prev_point = point
        cv2.line(img, (int(prev_point['x']), int(prev_point['y'])), (int(point['x']), int(point['y'])), (255, 0, 0), 5)
        prev_point = point


count = 0
while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.resize(img, (frameWidth, frameHeight))

    data = df.loc[df['count'] == count]
    if not data.empty:
        points = json.loads(data['points'].iloc[0])
        draw_overlay(points)
    
    cv2.imshow("Result", img)

    out.write(img)
    
    if cv2.waitKey(1) == ord('q'):
         break
    count+=1

cap.release()
out.release()
cv2.destroyAllWindows()
