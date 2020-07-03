import cv2
import numpy as np

frameWidth = 640
frameHeight = 480

kernel = np.ones((5, 5), np.uint8)

cap = cv2.VideoCapture("resources/object_detect_test_vid.mp4")

while True:
    success, img = cap.read()
    
    if not success:
        break
    
    img = cv2.resize(img, (frameWidth, frameHeight))
    img = cv2.Canny(img, 50, 50)

    cv2.imshow("Result", img)
    
    if cv2.waitKey(1) == ord('q'):
         break