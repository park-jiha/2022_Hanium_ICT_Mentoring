import json
from datetime import datetime
import time
from collections import OrderedDict
import json
import firebase_admin
from firebase_admin import messaging
from firebase_admin import credentials
 
credential_file_path = './greenfather.json'


def lambda_handler(event, context):
    cred = credentials.Certificate(credential_file_path)
    try:
        push_service = firebase_admin.get_app()
    except:
        push_service = firebase_admin.initialize_app(cred)
    topic_r = "on_road"
    topic_w = "danger_zone"
    topic_c = "c"
    
    dummy=OrderedDict()
    dummy={}
    if event==dummy:
        print('nothing')
    else:
        jsonData=[]
        for i in range(8):
            print(event[str(i)])
            #print(type(event[str(i)]))
            jsonData.append(event[str(i)])
        print(jsonData)
        
        if jsonData[0]==1:
            if jsonData[1]==1:
                if jsonData[2]==1:
                    message = messaging.Message(
                    data = {
                    'title': "도로 위에 사람 자전거 킥보드 위험!",
                    'body': "도로 위에 사람, 자전거, 킥보드가 있으니 주의해주세요",
                    'sound':'p_b_k_on_road'
                       },
                    topic = topic_r)
                else:
                    message = messaging.Message(
                    data = {
                    'title': "도로 위에 사람 자전거 위험!",
                    'body': "도로 위에 사람, 자전거가 있으니 주의해주세요",
                    'sound':'p_b_on_road'
                    },
                    topic = topic_r)
            else:
                if jsonData[2]==1:
                    message = messaging.Message(
                    data = {
                    'title': "도로 위에 사람 킥보드 위험!",
                    'body': "도로 위에 사람, 킥보드가 있으니 주의해주세요",
                    'sound':'p_k_on_road'
                    },
                    topic = topic_r)
                else:
                    message = messaging.Message(
                    data = {
                    'title': "도로 위에 사람 위험!",
                    'body': "도로 위에 사람이 있으니 주의해주세요",
                    'sound':'p_on_road'
                    },
                    topic = topic_r)
            response = messaging.send(message)
            print(str(message.data['body']).encode('utf-8'))
            
        if jsonData[1]==1:
            if jsonData[0]==0:
                if jsonData[2]==1:
                    message = messaging.Message(
                    data = {
                    'title': "도로 위에 자전거 킥보드 위험!",
                    'body': "도로 위에 자전거, 킥보드가 있으니 주의해주세요",
                    'sound':'b_k_on_road'
                    },
                    topic = topic_r)
                else:
                    message = messaging.Message(
                    data = {
                    'title': "도로 위에 자전거 위험!",
                    'body': "도로 위에 자전거가 있으니 주의해주세요",
                    'sound':'b_on_road'
                    },
                    topic = topic_r)
            response = messaging.send(message)
            print(str(message.data['body']).encode('utf-8'))
            
        if jsonData[2]==1:
            if jsonData[0]==0 and jsonData[1]==0:
                message = messaging.Message(
                data = {
                'title': "도로 위에 킥보드 위험!",
                'body': "도로 위에 킥보드가 있으니 주의해주세요",
                'sound':'k_on_road'
                },
                topic = topic_r)
            response = messaging.send(message)
            print(str(message.data['body']).encode('utf-8'))
        #if jsonData[0]==0 and jsonData[1]==0 and jsonData[2]==0:
        #    json_road_log=json_road_log+'None'
            
        if jsonData[3]==1:
            if jsonData[4]==1:
                if jsonData[5]==1:
                    if jsonData[6]==1:#사람 자전거 킥보드 오토바이
                        message = messaging.Message(
                        data = {
                        'title': "위험 지역 내에 사람 자전거 킥보드 오토바이 위험!",
                        'body': "위험 지역 내에 사람, 자전거, 킥보드, 오토바이가 있으니 주의해주세요",
                        'sound':'p_b_k_a_danger'
                        },
                        topic = topic_w)
                    else:#사람 자전거 킥보드
                        message = messaging.Message(
                        data = {
                        'title': "위험 지역 내에 사람 자전거 킥보드 위험!",
                        'body': "위험 지역 내에 사람, 자전거, 킥보드가 있으니 주의해주세요",
                        'sound':'p_b_k_danger'
                        },
                        topic = topic_w)
                else:
                    if jsonData[6]==1:#사람 자전거 오토바이
                        message = messaging.Message(
                        data = {
                        'title': "위험 지역 내에 사람 자전거 오토바이 위험!",
                        'body': "위험 지역 내에 사람, 자전거, 오토바이가 있으니 주의해주세요",
                        'sound':'p_b_a_danger'
                        },
                        topic = topic_w)
                    else:#사람 자전거
                        message = messaging.Message(
                        data = {
                        'title': "위험 지역 내에 사람 자전거 위험!",
                        'body': "위험 지역 내에 사람, 자전거가 있으니 주의해주세요",
                        'sound':'p_b_danger'
                        },
                        topic = topic_w)
                    
            else:
                if jsonData[5]==1:
                    if jsonData[6]==1:#사람 킥보드 오토바이
                        message = messaging.Message(
                        data = {
                        'title': "위험 지역 내에 사람 킥보드 오토바이 위험!",
                        'body': "위험 지역 내에 사람, 킥보드, 오토바이가 있으니 주의해주세요",
                        'sound':'p_k_a_danger'
                        },
                        topic = topic_w)
                    else:#사람 킥보드
                        message = messaging.Message(
                        data = {
                        'title': "위험 지역 내에 사람 킥보드 위험!",
                        'body': "위험 지역 내에 사람, 킥보드가 있으니 주의해주세요",
                        'sound':'p_k_danger'
                        },
                        topic = topic_w)
                else:
                    if jsonData[6]==1:#사람 오토바이
                        message = messaging.Message(
                        data = {
                        'title': "위험 지역 내에 사람 오토바이 위험!",
                        'body': "위험 지역 내에 사람, 오토바이가 있으니 주의해주세요",
                        'sound':'p_a_danger'
                        },
                        topic = topic_w)
                    else:#사람
                        message = messaging.Message(
                        data = {
                        'title': "위험 지역 내에 사람 위험!",
                        'body': "위험 지역 내에 사람이 있으니 주의해주세요",
                        'sound':'p_danger'
                        },
                        topic = topic_w)
                        
            response = messaging.send(message)
            print(str(message.data['body']).encode('utf-8'))
            
        if jsonData[4]==1:
            if jsonData[3]==0:
                if jsonData[5]==1:
                    if jsonData[6]==1:#자전거 킥보드 오토바이
                        message = messaging.Message(
                        data = {
                        'title': "위험 지역 내에 자전거 킥보드 오토바이 위험!",
                        'body': "위험 지역 내에 자전거, 킥보드, 오토바이가 있으니 주의해주세요",
                        'sound':'b_k_a_danger'
                        },
                        topic = topic_w)
                    else:#자전거 킥보드
                        message = messaging.Message(
                        data = {
                        'title': "위험 지역 내에 자전거 킥보드 위험!",
                        'body': "위험 지역 내에 자전거, 킥보드가 있으니 주의해주세요",
                        'sound':'b_k_danger'
                        },
                        topic = topic_w)
                else:
                    if jsonData[6]==1:#자전거 오토바이
                        message = messaging.Message(
                        data = {
                        'title': "위험 지역 내에 자전거 오토바이 위험!",
                        'body': "위험 지역 내에 자전거, 오토바이가 있으니 주의해주세요",
                        'sound':'b_a_danger'
                        },
                        topic = topic_w)
                    else:#자전거
                        message = messaging.Message(
                        data = {
                        'title': "위험 지역 내에 자전거 위험!",
                        'body': "위험 지역 내에 자전거가 있으니 주의해주세요",
                        'sound':'b_danger'
                        },
                        topic = topic_w)
                response = messaging.send(message)
                print(str(message.data['body']).encode('utf-8'))
        if jsonData[5]==1:
            if jsonData[3]==0 and jsonData[4]==0:
                if jsonData[6]==1:#킥보드 오토바이
                    message = messaging.Message(
                    data = {
                    'title': "위험 지역 내에 킥보드 오토바이 위험!",
                    'body': "위험 지역 내에 킥보드, 오토바이가 있으니 주의해주세요",
                    'sound':'k_a_danger'
                    },
                    topic = topic_w)
                
                else:#킥보드
                    message = messaging.Message(
                    data = {
                    'title': "위험 지역 내에 킥보드 위험!",
                    'body': "위험 지역 내에 킥보드가 있으니 주의해주세요",
                    'sound':'k_danger'
                    },
                    topic = topic_w)
                response = messaging.send(message)
                print(str(message.data['body']).encode('utf-8'))
            
        if jsonData[6]==1:
            if jsonData[3]==0 and jsonData[4]==0 and jsonData[5]==0:
                message = messaging.Message(
                data = {
                'title': "위험 지역 내에 오토바이 위험!",
                'body': "위험 지역 내에 오토바이가 있으니 주의해주세요",
                'sound':'a_danger'
                },
                topic = topic_w)
                response = messaging.send(message)
                print(str(message.data['body']).encode('utf-8'))
                
                
        #if jsonData[3]==0 and jsonData[4]==0 and jsonData[5]==0 and jsonData[6]==0:
        #    json_danger_log=json_danger_log+'None'
                    
                    
        if jsonData[7]==1:
            message = messaging.Message(
            data = {
            'title': "충돌 위험 !",
            'body': "충돌 위험 !",
            'sound':'c_alert'
            },
            topic = topic_w)
            response = messaging.send(message)
            print(str(message.data['body']).encode('utf-8'))
            
        #else:
        #    json_collision_log='None'
    print('new one')
    print(event)
    print(type(event)) #딕셔너리
    return event