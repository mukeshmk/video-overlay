import cv2
import numpy as np

frameWidth = 640
frameHeight = 480

def getContours(img):
    # contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 2000:
            cv2.drawContours(imgCont, cnt, -1, (255, 0, 0), 3)


kernel = np.ones((5, 5), np.uint8)

cap = cv2.VideoCapture("resources/object_detect_test_vid.mp4")

count = 0
while True:
    success, img = cap.read()
    
    if not success:
        break
    
    img = cv2.resize(img, (frameWidth, frameHeight))
    imgCont = img.copy()
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (7, 7), 1)
    img = cv2.Canny(img, 50, 50)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    
    getContours(img)

    cv2.imshow("Result", imgCont)

    cv2.imwrite("output/img-" + str(count) + ".jpg", imgCont)
    
    if cv2.waitKey(1) == ord('q') or count > 40:
         break
    count+=1

cv2.destroyAllWindows()
