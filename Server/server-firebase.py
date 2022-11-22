import boto3
import json
from datetime import datetime
import time
from collections import OrderedDict
import json
from pytz import timezone



ACCESS_KEY = ""
SECRET_KEY = ""
BUCKET_NAME = ""
URI = ""

iot_client = boto3.client('iot-data')
client = boto3.client('lambda')
s3 = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)
bucket = s3.Bucket(BUCKET_NAME)
def lambda_handler(event, context):
    jsonData_5=OrderedDict()
    null_json=0
    now = datetime.now(timezone('Asia/Seoul'))
    print("< current time : ",now," >")
    count=0
    for obj in bucket.objects.filter(Prefix = ""):
        key = obj.key
        print("< file list >")
        print("File name:",key)
        now = str(now)
        now=now[:19].replace(" ", "_")
        now=now.replace(":","_")
        year=int(now[:4])
        lunar=round(year/4)
        month=int(now[5:7])
        day=int(now[8:10])
        hour=int(now[11:13])
        min_=int(now[14:16])
        sec=int(now[17:19])
        months=[31,59,90,120,151,181,212,243,273,304,334,365]
        months_l=[31,60,91,121,152,182,213,244,274,305,335,366]
        if year%4!=0:
            sum_=sec+min_*60+hour*3600+day*3600*24+months[month-1]*3600*24+year*3600*24*365+lunar*3600*24
        else:
            sum_=sec+min_*60+hour*3600+day*3600*24+months_l[month-1]*3600*24+year*3600*24*365+lunar*3600*24
        print(sum_)
        if key.endswith('.json'):
            jsonName = key
            jsonURL = URI + jsonName
            jsonData = bucket.Object(jsonName).get()['Body'].read().decode('utf-8')
            if count==0:
                last_name=jsonName
            #print("< JSON info >")
            #print('file name:', jsonName)
            #print("file path:", jsonURL)
            #print("more info:", jsonData)
            #print(jsonData)
            b=jsonName
            jsonData=eval(jsonData)
            #print("file name:",b)
            b_year=int(b[4:8])
            b_month=int(b[9:11])
            b_day=int(b[12:14])
            b_hour=int(b[15:17])
            b_min=int(b[18:20])
            b_sec=int(b[21:23])
            b_lunar=round(b_year/4)
            b_name=b[4:23]
            if b_year%4!=0:
                b_sum=b_sec+b_min*60+b_hour*3600+b_day*3600*24+months[b_month-1]*3600*24+b_year*3600*24*365+b_lunar*3600*24
            else:
                b_sum=b_sec+b_min*60+b_hour*3600+b_day*3600*24+months_l[b_month-1]*3600*24+b_year*3600*24*365+b_lunar*3600*24
            print(b_sum)
            print(sum_," - ",b_sum," = ",(sum_-b_sum)," seconds")
            
            if sum_-b_sum<5:
                null_json=1
                print(jsonData)

                jsonData_5={
                    '0':jsonData[0],
                    '1':jsonData[1],
                    '2':jsonData[2],
                    '3':jsonData[3],
                    '4':jsonData[4],
                    '5':jsonData[5],
                    '6':jsonData[6],
                    '7':jsonData[7],
                    }
                
                json_road_log=''
                json_danger_log=''
                json_collision_log=''
                if jsonData[0]==1:
                    json_road_log=json_road_log+'person '
                    
                        
                if jsonData[1]==1:
                    json_road_log=json_road_log+'bicycle '
                   
                    
                if jsonData[2]==1:
                    json_road_log=json_road_log+'kickboard '
                    
                    
                if jsonData[0]==0 and jsonData[1]==0 and jsonData[2]==0:
                    json_road_log=json_road_log+'None'
                    
                if jsonData[3]==1:
                    json_danger_log=json_danger_log+'person '
                    
                    
                if jsonData[4]==1:
                    json_danger_log=json_danger_log+'bicycle '
                    
                    
                if jsonData[5]==1:
                    json_danger_log=json_danger_log+'kickboard '
                    
                    
                if jsonData[6]==1:
                    json_danger_log=json_danger_log+'motorbike '
                    
                if jsonData[3]==0 and jsonData[4]==0 and jsonData[5]==0 and jsonData[6]==0:
                    json_danger_log=json_danger_log+'None'
                    
                    
                if jsonData[7]==1:
                    json_collision_log='collision alert'
                    
                else:
                    json_collision_log='None'
                    
                json_payload='{'
                json_payload=json_payload+'\n   "File Name" : "'+jsonName+'",'
                json_payload=json_payload+'\n   "On road" : "'+json_road_log+'",'
                json_payload=json_payload+'\n   "In danger zone" : "'+json_danger_log+'",'
                json_payload=json_payload+'\n   "Collision risk" : "'+json_collision_log+'"\n}'
                response = iot_client.publish(
                topic='green/camera_01',
                qos=0,
                payload=json_payload.encode(),
                )


                

                
        count+=1
        if count>=6:
            s3.Object(BUCKET_NAME, last_name).delete()
            print("Last file deleted: " +last_name)
            count-=1
    print("=========end of file=========")
    if null_json==0:
        print('nothing')
        jsonData_5={
            
        }
    response_lambda = client.invoke(
    FunctionName = '',
    InvocationType = 'RequestResponse',
    Payload = json.dumps(jsonData_5)
    )
    responseFromChild = json.load(response_lambda['Payload'])
    print(responseFromChild)