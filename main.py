import cv2
import numpy as np

cap = cv2.VideoCapture('carsVideo.mp4')

fgbg = cv2.createBackgroundSubtractorMOG2()
output_width = 640
output_height = 480

while True:
    ret, frame = cap.read()

    if not ret:
        break
    
    frame = cv2.resize(frame, (output_width, output_height))
    fgmask = fgbg.apply(frame)

    blur = cv2.GaussianBlur(fgmask, (5, 5), 0)

    _, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)

        if area > 100:
           
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Object Detection', frame)
    cv2.waitKey(20)

    if cv2.waitKey(1) & 0xFF == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()
