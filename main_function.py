import cv2 as cv
import numpy as np
import math
from shapely.geometry import Point, Polygon  # 기하학적 물체 표현

road_x = np.array(
    [[4, 1076], [1532, 1074], [1886, 324], [1606, 154], [1552, 162], [1656, 332], [1594, 388], [1324, 430], [1186, 416],
     [768, 318], [794, 296], [688, 266], [664, 276], [692, 348], [1046, 488], [1058, 574]])

ROI = Polygon(road_x)

road_x_ = np.array(
    [[1260, 708], [1288, 564], [1128, 370], [804, 208], [800, 258], [1096, 424], [1130, 470], [1122, 512], [1090, 542],
     [804, 698], [764, 680], [618, 754], [644, 790], [844, 756], [1118, 578], [1186, 586]])

''' 주정차 임의로 찍은거라 일단 위험지역은 다 주석처리 했음
ROI_1 = Polygon([[12, 1132], [12, 2148], [3836, 2156], [3836, 888]])
ROI_2 = Polygon([[12, 1132], [12, 2148], [3836, 2156], [3836, 888]])
ROI_3 = Polygon([[12, 1132], [12, 2148], [3836, 2156], [3836, 888]])
'''

# Calculate Homography
h_, status = cv.findHomography(road_x, road_x_)
mppix = 3/36.1 # 1픽셀당 몇 미터인지 ==> 0.08미터, 3/math.sqrt((1155-1125)**2 + (565-585)**2)

while True:
    result = [0, 0, 0, 0, 0, 0, 0]  # 차도 사람, 자전거, 오토바이, 위험지역 사람, 자전거, 오토바이, 충돌위험
    in_driveway = []  # 차도 영역 내 객체 리스트, 차 <-> 오토바이,자전거랑 거리도 계산하게 했음
    car = []

    '''검출 결과 얻기'''

    # vehicle -> 박스 중점 / 나머지 -> 하단 중점
    if name == 'car':
        point = ([(xmin + xmax) // 2, (ymin + ymax) // 2])

        new_veh_x = (h_[0][0] * point[0] + h_[0][1] * point[1] + h_[0][2]) / (
                h_[2][0] * point[0] + h_[2][1] * point[1] + 1)
        new_veh_y = (h_[1][0] * point[0] + h_[1][1] * point[1] + h_[1][2]) / (
                h_[2][0] * point[0] + h_[2][1] * point[1] + 1)

        car.append([new_veh_x, new_veh_y])

    elif name == 'person':
        point = ([(xmin + xmax) // 2, ymax])

    ### 차도 영역 내 보행자 판단
        ped = Point(point[0], point[1])

        if ped.within(ROI) == 1:
            print("경고! 차도 내 보행자가 위치합니다!")
            result[0] += 1

            new_ped_x = (h_[0][0] * point[0] + h_[0][1] * point[1] + h_[0][2]) / (
                    h_[2][0] * point[0] + h_[2][1] * point[1] + 1)
            new_ped_y = (h_[1][0] * point[0] + h_[1][1] * point[1] + h_[1][2]) / (
                    h_[2][0] * point[0] + h_[2][1] * point[1] + 1)
            in_driveway.append([new_ped_x, new_ped_y])
        else:
            print("안전! 차도 내 보행자가 없습니다.")

    '''위험 지역 내 보행자 판단
        if ped.within(ROI_1) or ped.within(ROI_2) or ped.within(ROI_3) == 1:
            print("경고! 위험구역 내 보행자가 위치합니다!")
            # result[3] += 1
        else:
            print("안전! 위험구역 내 보행자가 없습니다.")'''

    elif name == 'bicycle':
        point = ([(xmin + xmax) // 2, ymax])

        ### 차도 영역 내 자전거 판단
        cyc = Point(point[0], point[1])

        if cyc.within(ROI) == 1:
            print("경고! 차도 내 자전거가 위치합니다!")
            result[1] += 1

            new_cyc_x = (h_[0][0] * point[0] + h_[0][1] * point[1] + h_[0][2]) / (
                    h_[2][0] * point[0] + h_[2][1] * point[1] + 1)
            new_cyc_y = (h_[1][0] * point[0] + h_[1][1] * point[1] + h_[1][2]) / (
                    h_[2][0] * point[0] + h_[2][1] * point[1] + 1)
            in_driveway.append([new_cyc_x, new_cyc_y])
        else:
            print("안전! 차도 내 자전거가 없습니다.")

        '''위험 지역 내 보행자 판단
        if ped.within(ROI_1) or ped.within(ROI_2) or ped.within(ROI_3) == 1:
            print("경고! 위험구역 내 보행자가 위치합니다!")
            # result[4] += 1
        else:
            print("안전! 위험구역 내 보행자가 없습니다.")'''

    elif name == 'motorcycle':
        point = ([(xmin + xmax) // 2, ymax])

        moto = Point(point[0], point[1])

        if moto.within(ROI) == 1:
            print("경고! 차도 내 오토바이가 위치합니다!")
            result[2] += 1

            new_moto_x = (h_[0][0] * point[0] + h_[0][1] * point[1] + h_[0][2]) / (
                    h_[2][0] * point[0] + h_[2][1] * point[1] + 1)
            new_moto_y = (h_[1][0] * point[0] + h_[1][1] * point[1] + h_[1][2]) / (
                    h_[2][0] * point[0] + h_[2][1] * point[1] + 1)
            in_driveway.append([new_moto_x, new_moto_y])
        else:
            print("안전! 차도 내 오토바이가 없습니다.")

    '''위험 지역 내 보행자 판단
        if ped.within(ROI_1) or ped.within(ROI_2) or ped.within(ROI_3) == 1:
            print("경고! 위험구역 내 보행자가 위치합니다!")
            # result[5] += 1
        else:
            print("안전! 위험구역 내 보행자가 없습니다.")'''

    while car:
        ccar = car.pop()
        for i in range(len(in_driveway)):
            dis = math.sqrt((in_driveway[i][0] - ccar[0]) ** 2 + ((in_driveway[i][1] - ccar[1]) ** 2)) * mppix
            if dis < 50:
                print("위험! 충돌 위험 객체가 있습니다! (위치 좌표 :", new_veh_x, ",", new_veh_y, ")")
                result[6] += 1
            else:
                print("안전! 충돌 위험 객체가 없습니다. (위치 좌표 :", new_veh_x, ",", new_veh_y, ")")

    # 뒤에 서버 전송