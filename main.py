import cv2
import pandas as pd
from ultralytics import YOLO
from tracker import *
import numpy as np
import time

model = YOLO('yolov8s.pt')

def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        colorsBGR = [x, y]
        print(colorsBGR)

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

cap = cv2.VideoCapture(r"traffic22.mp4")

my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")

count = 0

tracker = Tracker()

cy1 = 322
cy2 = 368
offset = 6

speed_limit = 50 # in km/h
pixels_per_meter = 5.5
time_window = 0.002 # in seconds

previous_frame_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    count += 1
    if count % 3 != 0:
        continue
    frame = cv2.resize(frame, (1020, 500))

    results = model.predict(frame)
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")
    list = []

    for index, row in px.iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])
        c = class_list[d]
        if ('car' in c) or ('bus' in c) or ('truck' in c):
            list.append([x1, y1, x2, y2])

    current_frame_time = time.time()
    time_difference = current_frame_time - previous_frame_time

    if time_difference > time_window:
        previous_frame_time = current_frame_time
        bbox_id = tracker.update(list)
        for bbox in bbox_id:
            x3, y3, x4, y4, id = bbox
            cx = int(x3 + x4) // 2
            cy = int(y3 + y4) // 2
            speed = speed_limit * pixels_per_meter / time_difference / 100 * 2.5
            cv2.putText(frame, "Speed: " + str(int(speed)) + " km/h", (cx, cy), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 255), 1)
            cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
            cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)
    else:
        tracker.update(list)
    cv2.imshow("RGB", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
