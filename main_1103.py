#!/usr/bin/env python
# coding: utf-8

# In[1]:


import torch
import cv2
import numpy as np
import pandas as pd
import math
from shapely.geometry import Point, Polygon  # 기하학적 물체 표현

road_x = np.array(
    [[0, 1080], [1490, 1080], [1975, 350], [1680, 210], [1585, 225], [1625, 340], [1525, 395], [1240, 410], [875, 310], [775, 365],
     [1030, 465], [1030, 585], [0, 1000]])

ROI = Polygon(road_x)

road_x_ = np.array(
    [[1715, 960], [1775, 635], [1125, 205], [245, 0], [150, 85], [850, 300], [1005, 385], [1000, 495], [55, 805], [155, 920],
     [955, 665], [1385, 725], [1680, 985]])

# 주정차 임의로 찍은거라 일단 위험지역은 다 주석처리 했음
parking = [[305,850], [765,850], [765,1080], [305,1080]]
center_parking = [(305+765)/2, (850+1080)/2]
# ROI_2 = Polygon([[12, 1132], [12, 2148], [3836, 2156], [3836, 888]])
# ROI_3 = Polygon([[12, 1132], [12, 2148], [3836, 2156], [3836, 888]])


# Calculate Homography
h_, status = cv2.findHomography(road_x, road_x_)
mppix = 4.2/ 119.3# 1픽셀당 몇 미터인지 ==> 0.0352미터, 3/math.sqrt((1095-995)**2 + (480-545)**2)
h_parking = [(h_[0][0] * center_parking[0] + h_[0][1] * center_parking[1] + h_[0][2]) / (h_[2][0] * center_parking[0] + h_[2][1] * center_parking[1] + 1),
             (h_[1][0] * center_parking[0] + h_[1][1] * center_parking[1] + h_[1][2]) / (h_[2][0] * center_parking[0] + h_[2][1] * center_parking[1] + 1)]
# Model
# model = torch.hub.load('.', 'custom', path='./runs/train/exp11/weights/best.pt', source='local')
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

video_path = './video/school_1.mp4'

cap = cv2.VideoCapture(video_path)

if not cap.isOpened:
    print('--(!)Error opening video capture')
    sys.exit(1)

    
while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        break
        
    # Inference
    results = model(image)
    
#     print(results.pandas().xyxy[0])
#     for k in range(len(results.xyxy[0])):
#         print(results.pandas().xyxy[0].name[k])
#     break

    for k in range(len(results.xyxy[0])):
        conf = results.pandas().xyxy[0].confidence[0]*100
        if conf >= 50:
            if results.pandas().xyxy[0].name[k] == 'person':
                label = "person: {:.2f}".format(conf)
                color_g = (0, 255, 0)
                cv2.rectangle(image, (int(results.pandas().xyxy[0].xmin[k]), int(results.pandas().xyxy[0].ymin[k])), (int(results.pandas().xyxy[0].xmax[k]), int(results.pandas().xyxy[0].ymax[k])), color_g, 2)
                cv2.putText(image, label, (int(results.pandas().xyxy[0].xmin[k]), int(results.pandas().xyxy[0].ymin[k] - 5)), cv2.FONT_HERSHEY_DUPLEX, 1, color_g, 1)
            elif results.pandas().xyxy[0].name[k] == 'car':
                label = "car: {:.2f}".format(conf)
                color_y = (255, 255, 0)
                cv2.rectangle(image, (int(results.pandas().xyxy[0].xmin[k]), int(results.pandas().xyxy[0].ymin[k])), (int(results.pandas().xyxy[0].xmax[k]), int(results.pandas().xyxy[0].ymax[k])), color_y, 2)
                cv2.putText(image, label, (int(results.pandas().xyxy[0].xmin[k]), int(results.pandas().xyxy[0].ymin[k] - 5)), cv2.FONT_HERSHEY_DUPLEX, 1, color_y, 1)
            elif results.pandas().xyxy[0].name[k] == 'bicycle':
                label = "bycycle: {:.2f}".format(conf)
                color_b = (0, 0, 255)
                cv2.rectangle(image, (int(results.pandas().xyxy[0].xmin[k]), int(results.pandas().xyxy[0].ymin[k])), (int(results.pandas().xyxy[0].xmax[k]), int(results.pandas().xyxy[0].ymax[k])), color_b, 2)
                cv2.putText(image, label, (int(results.pandas().xyxy[0].xmin[k]), int(results.pandas().xyxy[0].ymin[k] - 5)), cv2.FONT_HERSHEY_DUPLEX, 1, color_b, 1)
            elif results.pandas().xyxy[0].name[k] == 'motorcycle':
                label = "motorcycle: {:.2f}".format(conf)
                color_p = (128, 0, 128)
                cv2.rectangle(image, (int(results.pandas().xyxy[0].xmin[k]), int(results.pandas().xyxy[0].ymin[k])), (int(results.pandas().xyxy[0].xmax[k]), int(results.pandas().xyxy[0].ymax[k])), color_p, 2)
                cv2.putText(image, label, (int(results.pandas().xyxy[0].xmin[k]), int(results.pandas().xyxy[0].ymin[k] - 5)), cv2.FONT_HERSHEY_DUPLEX, 1, color_p, 1)
            else: continue
    
   
    # 기능 시작
    result = [0, 0, 0, 0, 0, 0, 0]  # 차도 사람, 자전거, 오토바이, 위험지역 사람, 자전거, 오토바이, 충돌위험
    in_driveway = []  # 차도 영역 내 객체 리스트, 차 <-> 오토바이,자전거랑 거리도 계산하게 했음
    car = []

    
    for k in range(len(results.xyxy[0])):
        conf = results.pandas().xyxy[0].confidence[0]*100
        if conf >= 50:
            # vehicle -> 박스 중점 / 나머지 -> 하단 중점
            if results.pandas().xyxy[0].name[k] == 'car':
                point = ([(int(results.pandas().xyxy[0].xmin[k]) + int(results.pandas().xyxy[0].xmax[k]) // 2), (int(results.pandas().xyxy[0].ymin[k]) + int(results.pandas().xyxy[0].ymax[k]) // 2)])

                new_veh_x = (h_[0][0] * point[0] + h_[0][1] * point[1] + h_[0][2]) / (
                        h_[2][0] * point[0] + h_[2][1] * point[1] + 1)
                new_veh_y = (h_[1][0] * point[0] + h_[1][1] * point[1] + h_[1][2]) / (
                        h_[2][0] * point[0] + h_[2][1] * point[1] + 1)

                car.append([new_veh_x, new_veh_y])

            elif results.pandas().xyxy[0].name[k] == 'person':
                point = ([(int(results.pandas().xyxy[0].xmin[k]) + int(results.pandas().xyxy[0].xmax[k]) // 2), int(results.pandas().xyxy[0].ymax[k])])

                ### 차도 영역 내 보행자 판단
                ped = Point(point[0], point[1])
                new_ped_x = (h_[0][0] * point[0] + h_[0][1] * point[1] + h_[0][2]) / (
                        h_[2][0] * point[0] + h_[2][1] * point[1] + 1)
                new_ped_y = (h_[1][0] * point[0] + h_[1][1] * point[1] + h_[1][2]) / (
                        h_[2][0] * point[0] + h_[2][1] * point[1] + 1)

                if ped.within(ROI) == 1:
                    print("경고! 차도 내 보행자가 위치합니다!")
                    result[0] += 1
                    in_driveway.append([new_ped_x, new_ped_y])
                else:
                    print("안전! 차도 내 보행자가 없습니다.")

                if math.sqrt(((new_ped_x - h_parking[0]) ** 2) + ((new_ped_y - h_parking[1]) ** 2)) * mppix <= 3:
                    print("경고! 위험구역 내 보행자가 위치합니다!")
                    result[3] += 1
                else:
                    print("안전! 위험구역 내 보행자가 없습니다.")

             #위험 지역 내 보행자 판단


            elif results.pandas().xyxy[0].name[k] == 'bicycle':
                point = ([(int(results.pandas().xyxy[0].xmin[k]) + int(results.pandas().xyxy[0].xmax[k]) // 2), int(results.pandas().xyxy[0].ymax[k])])

                ### 차도 영역 내 자전거 판단
                cyc = Point(point[0], point[1])
                new_cyc_x = (h_[0][0] * point[0] + h_[0][1] * point[1] + h_[0][2]) / (
                        h_[2][0] * point[0] + h_[2][1] * point[1] + 1)
                new_cyc_y = (h_[1][0] * point[0] + h_[1][1] * point[1] + h_[1][2]) / (
                        h_[2][0] * point[0] + h_[2][1] * point[1] + 1)
                in_driveway.append([new_cyc_x, new_cyc_y])

                if cyc.within(ROI) == 1:
                    #print("경고! 차도 내 자전거가 위치합니다!")
                    result[1] += 1
                else:
                    print("안전! 차도 내 자전거가 없습니다.")

                if math.sqrt(((new_cyc_x - h_parking[0]) ** 2) + ((new_cyc_y - h_parking[1]) ** 2)) * mppix <= 3:
                    print("경고! 위험구역 내 자전거가 위치합니다!")
                    result[4] += 1
                else:
                    print("안전! 위험구역 내 자전거가 없습니다.")

                 #위험 지역 내 보행자 판단


            elif results.pandas().xyxy[0].name[k] == 'motorcycle':
                point = ([(int(results.pandas().xyxy[0].xmin[k]) + int(results.pandas().xyxy[0].xmax[k]) // 2), int(results.pandas().xyxy[0].ymax[k])])

                moto = Point(point[0], point[1])
                new_moto_x = (h_[0][0] * point[0] + h_[0][1] * point[1] + h_[0][2]) / (
                        h_[2][0] * point[0] + h_[2][1] * point[1] + 1)
                new_moto_y = (h_[1][0] * point[0] + h_[1][1] * point[1] + h_[1][2]) / (
                        h_[2][0] * point[0] + h_[2][1] * point[1] + 1)
                in_driveway.append([new_moto_x, new_moto_y])

                if moto.within(ROI) == 1:
                    print("경고! 차도 내 오토바이가 위치합니다!")
                    result[2] += 1
                else:
                    print("안전! 차도 내 오토바이가 없습니다.")

             #위험 지역 내 보행자 판단
                if math.sqrt(((new_moto_x - h_parking[0]) ** 2) + ((new_moto_y - h_parking[1]) ** 2)) * mppix <= 3:
                    print("경고! 위험구역 내 오토바이가 위치합니다!")
                    result[5] += 1
                else:
                    print("안전! 위험구역 내 오토바이가 없습니다.")
    
    while car:
        ccar = car.pop()
        for i in range(len(in_driveway)):
            dis = math.sqrt(((in_driveway[i][0] - ccar[0]) ** 2) + ((in_driveway[i][1] - ccar[1]) ** 2)) * mppix
            if dis < 50:
                print("위험! 충돌 위험 객체가 있습니다! (위치 좌표 :", str(in_driveway[i][0]), ",", str(in_driveway[i][1]), ")")
                result[6] += 1
            else:
                print("안전! 충돌 위험 객체가 없습니다. (위치 좌표 :", str(ccar[0]), ",", str(ccar[1]), ")")

    print("@@@ result @@@", result)
                               
    # Results
    cv2.imshow('Detection', image)
    
    key_pressed = cv2.waitKey(1) & 0xFF
    if key_pressed == ord('q') or key_pressed == 27:
        break

cap.release()
cv2.destroyAllWindows()

                
# 뒤에 서버 전송


# In[ ]:


