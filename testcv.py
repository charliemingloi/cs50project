import cv2 as cv

#image1 = cv.imread('download.jpeg')

#cv.imshow('new' , image1)

capture = cv.VideoCapture(0)

while True:
    isTrue, frame = capture.read()
    cv.imshow('cam' , frame)

    if cv.waitKey(20) &0xFF==ord('d'):
        break
    
capture.release()
cv.destroyAllWindows()