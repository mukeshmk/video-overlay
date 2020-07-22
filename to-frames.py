import cv2
import numpy as np
import json
import pandas as pd

frameWidth = 640
frameHeight = 480

cap = cv2.VideoCapture("resources/object_detect_test_vid.mp4")
cap.set(cv2.CAP_PROP_FPS, 20)

def saveImg(count, img):
    cv2.imwrite("output/frames/img-" + str(count) + ".jpg", img)

count = 0
while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.resize(img, (frameWidth, frameHeight))

    saveImg(count, img)
    
    cv2.imshow("Result", img)
    
    if cv2.waitKey(1) == ord('q'):
         break
    count+=1

cap.release()
cv2.destroyAllWindows()
