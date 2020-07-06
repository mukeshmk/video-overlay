import cv2
import numpy as np
import json
import pandas as pd

frameWidth = 640
frameHeight = 480

cap = cv2.VideoCapture("resources/object_detect_test_vid.mp4")
df = pd.read_csv('resources/required-data.csv')

out = cv2.VideoWriter('output/output.mp4', -1, 20.0, (frameWidth, frameHeight))

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
    points = json.loads(data['points'].iloc[0])
    draw_overlay(points)
    
    cv2.imshow("Result", img)

    out.write(img)
    
    if cv2.waitKey(1) == ord('q') or count > 40:
         break
    count+=1

cap.release()
out.release()
cv2.destroyAllWindows()
