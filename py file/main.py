import cv2 as cv
from ultralytics import YOLO

#model
model = YOLO('yolov8n.pt')
plate_detector = YOLO('./models/license_plate_detector.pt')

#main

capture = cvVideoCapture(0)

while True:
    isTrue, frame = capture.read()
    cv.imshow('cam', frame)
    