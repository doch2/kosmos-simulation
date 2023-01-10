# -*- coding: utf-8 -*-
import cv2
import numpy as np
import time

#YOLO Model Setting
net = cv2.dnn.readNet("yolov3.cfg","yolov3.weights")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))


cap = cv2.VideoCapture(0)
if cap.isOpened():
    while True:
        ret, img = cap.read()
        if ret:
            cv2.imshow("Original Camera",img) #프레임 이미지 표시

            img2 = cv2.resize(img, None, fx=0.4, fy=0.4)
            height, width, channels = img2.shape

            # Detecting objects
            blob = cv2.dnn.blobFromImage(img2, 0.001, (416, 416), (0, 0, 0))
            net.setInput(blob)
            outs = net.forward(output_layers)

            class_ids = []
            confidences = []
            boxes = []
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5 and class_id == 0:
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        # 좌표
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
                        
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            print("인식되고 있는 사람 수: " + len(indexes)) #### 사람수 


            font = cv2.FONT_HERSHEY_PLAIN
            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(classes[class_ids[i]])
                    color = colors[i]
                    cv2.rectangle(img2, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(img2, label, (x, y + 30), font, 3, color, 3)
                    
            import matplotlib.pyplot as plt
            cv2.imshow("People Recognition Camera", img2)


            if cv2.waitKey(1) != -1:
                break
        else:
            print("no fram")
            break
        
        #time.sleep(0.1)
else:
    print("can't open camera")
cap.release()
cv2.destroyAllWindows()