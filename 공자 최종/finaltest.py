import sys
import xgboost as xgb
from csv import reader
import pandas as pd
import datetime as dt
import numpy as np
import datetime
import pytz
import urllib.request
import pandas as pd
import json
from dateutil.parser import parse
from operator import eq 
import requests
import math

sys.path.append(r'C:\Users\mhmrm\Anaconda3\lib\site-packages\.')
sys.path.append(r'C:\Users\mhmrm\Anaconda3\xgboost')

#print(sys.argv[1]); # 162. 대여소번호
num = sys.argv[1]  # 대여소번호 

num1 = sys.argv[1]
num1 = str(num1)

#--------------------------------------
# 현재 대수
def bike_station():
    # str 형태로 들어가야함
    stationName= num1
    
    URL = 'http://openapi.seoul.go.kr:8088/415176436a6d686d383564506e584f/json/bikeList/1/1000/' 
    response = requests.get(URL)
    # response.status_code 
    # response.text
    data = urllib.request.urlopen(URL).read().decode('utf8')
    data_json = json.loads(data)
    # print(data_json)
    parsed_json = data_json['rentBikeStatus']['row']
    
    
    # print(parsed_json)
    for one_parsed in parsed_json:
        stopName=one_parsed['stationName']
        num = stopName.split(".")
        if str(num[0]) == stationName:              
            return one_parsed['parkingBikeTotCnt']
        
left = bike_station()








#--------------------------------------
# 날씨 받음

def get_api_date() :
    standard_time = [30,130, 230, 330, 430, 530, 630, 730, 830, 930, 1030, 1130, 1230, 1330, 1430, 1530, 1630, 1730, 1830, 1930, 2030, 2130, 2230, 2330]
    time_now = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime('%H%M')
#    print(time_now)
    check_time = int(time_now)
#    print(check_time)
    day_calibrate = 0
    while not check_time in standard_time :
        minute=check_time%100
        if minute>30:
            result= abs(minute-30)
#            print(result)
            check_time -=result
#            print(check_time)
        else:
            check_time-=minute
            check_time-=30
            
        

    date_now = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime('%Y%m%d')
    check_date = int(date_now) - day_calibrate
    if len(str(check_time)) == 2:
        return((str(check_date), ('00'+str(check_time))))
    elif len(str(check_time)) == 3 :
        return((str(check_date), ('0'+str(check_time))))
    else: 
        return (str(check_date), (str(check_time)))

def get_weather_data() :
    api_date, api_time = get_api_date()
    url = "http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastTimeData?"
    key = "serviceKey=" +"Dtazb4cOCAo84N7My73qz4bR9Abn8DL05NU%2Bmdf6Lo1K4mZgOaRccuP%2FIZoZdOyYC98LlKjvHJhcMQiEfiZ7yg%3D%3D"
    date = "&base_date=" + api_date
    time = "&base_time=" + api_time
#    print(api_time)
    
    nx = "&nx=60"
    ny = "&ny=127"
    numOfRows = "&numOfRows=100"
    type = "&_type=json"
    api_url = url + key + date + time + nx + ny + numOfRows + type
#     print(api_url)

    data = urllib.request.urlopen(api_url).read().decode('utf8')
    data_json = json.loads(data)


    parsed_json = data_json['response']['body']['items']['item']
    target_date = parsed_json[0]['fcstDate']  # get date and time
    target_time = parsed_json[0]['fcstTime']

    date_calibrate = target_date #date of TMX, TMN
   

    passing_data = {}
    for one_parsed in parsed_json:
        if one_parsed['fcstDate'] == target_date and one_parsed['fcstTime'] == target_time: #get today's data
            passing_data[one_parsed['category']] = one_parsed['fcstValue']

        if one_parsed['fcstDate'] == date_calibrate and (
                one_parsed['category'] == 'TMX' or one_parsed['category'] == 'TMN'): #TMX, TMN at calibrated day
            passing_data[one_parsed['category']] = one_parsed['fcstValue']

    return passing_data

if __name__ == '__main__':
    data = get_weather_data()

#--------------------------------------





features = ['년','월', '시', 
           '기온(°C)','강수량(mm)', '풍속(m/s)', 
           '습도(%)', '적설(cm)','요일_0', '요일_1', 
           '요일_2', '요일_3','요일_4', '요일_5', '요일_6',]


#datenow = sys.argv[2] # 지금 날짜, 시간
#datenow = pd.to_datetime(datenow, errors = 'coerce')

datenow = datetime.datetime.now()

# 18.7.20 16시
test = pd.DataFrame()
test.loc[0,'년'] = datenow.year-2010
test.loc[0,'월'] = datenow.month
test.loc[0,'시'] = datenow.hour

df = pd.DataFrame()
df.loc[0, '기온(°C)'] = data['T1H']
df.loc[0, '강수량(mm)'] = data['RN1']
df.loc[0, '풍속(m/s)'] = data['WSD']
df.loc[0, '습도(%)'] = data['REH']
df.loc[0, '적설(cm)'] = 0

test = pd.concat([test, df], axis = 1)

test['요일_0'] = 0
test['요일_1'] = 0
test['요일_2'] = 0
test['요일_3'] = 0
test['요일_4'] = 0
test['요일_5'] = 0
test['요일_6'] = 0

weekd = datenow.weekday # 요일
if weekd == 0:
    test.loc[0, '요일_0'] = 1
if weekd == 1:
    test.loc[0, '요일_1'] = 1
if weekd == 2:
    test.loc[0, '요일_2'] = 1
if weekd == 3:
    test.loc[0, '요일_3'] = 1
if weekd == 4:
    test.loc[0, '요일_4'] = 1 
if weekd == 5:
    test.loc[0, '요일_5'] = 1
if weekd == 6:
    test.loc[0, '요일_6'] = 1

    



# 저장된 모델 로드해서 테스트
loaded_model1 = xgb.Booster()
loaded_model1.load_model("data/model/수요" + str(int(num)) + ".model")

loaded_model2 = xgb.Booster()
loaded_model2.load_model("data/model/공급" + str(int(num)) + ".model")

dtest = xgb.DMatrix(test)

predictions1 = loaded_model1.predict(dtest)
predictions2 = loaded_model2.predict(dtest)



print(int(np.round(predictions1)))   #result1. 수요

print(int(np.round(predictions2)))   # result2. 공급

prediction = predictions2 - predictions1 # 공급 - 수요
print(int(np.round(prediction)))    # result3
print(left)          # 현재 남은 대수.


a = int(left)+prediction
# 수요가 더 많을 때. 자전거 모자랄 때
if prediction < 0:      
    #현재 대수가 충분한 경우
    if a > 2:       # ok
        print('enough. amount')
        print(int(np.round(a-2)))
    # 현재 대수가 모자란 경우. 리필 필요
    else:           # ok
        print('lack. amount')
        print(int(np.round((a-2)*(-1))))

# 공급이 더 많을 때. 자전거 남음
else:
    if a < 2:       # ok
        print('lack. amount')
        print(int(np.round((a-2)*(-1))))
        
    else:           # ok
        print('enough. amount')
        print(int(np.round(a-2)))
print(num)