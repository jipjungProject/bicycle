import sys
import pandas as pd
import datetime as dt
import numpy as np
import datetime
import pytz
import urllib.request
import json
from dateutil.parser import parse
from bs4 import BeautifulSoup
from operator import eq 
import requests
import xgboost as xgb

# sys.path.append(r'C:\Users\romaa\Anaconda3\xgboost')
#print(sys.argv[1]); # 162. 대여소번호

num1 = np.array([221, 342, 568, 216, 316, 210, 340, 326, 106, 259,
                   302, 639, 540, 341, 212, 222, 336, 116, 124, 385,
                   247, 162, 329, 118, 128, 346, 907, 144, 529, 501])

myList=[[0 for i in range(30)]for j in range(30)]

#--------------------------------------
# 현재 대수
a={}
def bike_station():
    # str 형태로 들어가야함
    
    URL = 'http://openapi.seoul.go.kr:8088/415176436a6d686d383564506e584f/json/bikeList/1/1000/' 
    response = requests.get(URL)
    # response.status_code 
    # response.text
    data = urllib.request.urlopen(URL).read().decode('utf8')
    data_json = json.loads(data)
    parsed_json = data_json['rentBikeStatus']['row']

    k=0
    for k in range(0,30):
        
        for one_parsed in parsed_json:
        
            stationName = str(num1[k])
            stopName=one_parsed['stationName']
            num = stopName.split(".")
            if str(num[0]) == stationName:
                s = int(one_parsed['parkingBikeTotCnt'])
                a[stationName] = s
                #(int(one_parsed['parkingBikeTotCnt']))
                break

        
bike_station()
b = []
for i in range(30):
    b.append(a['%d'%num1[i]])

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

#     print(data_json)
    parsed_json = data_json['response']['body']['items']['item']
#     print("============")
#     print(parsed_json)
#     print(parsed_json[0])
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


# 미세먼지 모델 끝나면 이거 넣으면 됨
#df.loc[0, '미세먼지'] = pm10
#df.loc[0, '초미세먼지'] = pm25

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

rental = np.array([221, 342, 568, 216, 316,
                   210, 340, 326, 106, 259,
                   302, 639, 540, 341, 212,
                   222, 336, 116, 124, 385,
                   247, 162, 329, 118, 128,
                   346, 907, 144, 529, 501])

distances = [[9999,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29],
             [0,9999,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29],
             [0,1,9999,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29],
             [0,1,2,9999,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29],
             [0,1,2,3,9999,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29],
             [0,1,2,3,4,9999,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29],
             [0,1,2,3,4,5,9999,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29],
             [0,1,2,3,4,5,6,9999,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29],
             [0,1,2,3,4,5,6,7,9999,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29],
             [0,1,2,3,4,5,6,7,8,9999,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29],
             [0,1,2,3,4,5,6,7,8,9,9999,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29],
             [0,1,2,3,4,5,6,7,8,9,10,9999,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29],
             [0,1,2,3,4,5,6,7,8,9,10,11,9999,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29],
             [0,1,2,3,4,5,6,7,8,9,10,11,12,9999,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29],
             [0,1,2,3,4,5,6,7,8,9,10,11,12,13,9999,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29],
             [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,9999,16,17,18,19,20,21,22,23,24,25,26,27,28,29],
             [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,9999,17,18,19,20,21,22,23,24,25,26,27,28,29],
             [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,9999,18,19,20,21,22,23,24,25,26,27,28,29],
             [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,9999,19,20,21,22,23,24,25,26,27,28,29],
             [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,9999,20,21,22,23,24,25,26,27,28,29],
             [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,9999,21,22,23,24,25,26,27,28,29],
             [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,9999,22,23,24,25,26,27,28,29],
             [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,9999,23,24,25,26,27,28,29],
             [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,9999,24,25,26,27,28,29],
             [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,9999,25,26,27,28,29],
             [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,9999,26,27,28,29],
             [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,9999,27,28,29],
             [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,9999,28,29],
             [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,9999,29],
             [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,9999]]

cur = b

dis = np.array(distances)

#print(cur)

message = []

pred = []

for i in range(30):
    location = rental[i]
    loaded_model = xgb.Booster()
    loaded_modelr = xgb.Booster()

    loaded_model.load_model("data/model/수요" + str(int(location)) + ".model")
    loaded_modelr.load_model("data/model/공급" + str(int(location)) + ".model")

    dtests = xgb.DMatrix(test)
    dtestr = xgb.DMatrix(test)

    predictions = loaded_model.predict(dtests)
    predictionsr = loaded_modelr.predict(dtestr)
    pred.append((predictionsr-predictions)[0])

#print(pred)

def route():
    for i in range(30):
        if round(cur[i] + pred[i]) < 2:
            tempdis = []
            nr = 1
            for a in range(len(pred)):
                if check(i, a+1)==True:
                    nr = a+1
                    break
            t = [-1 for i in range(nr)]
            for rout in range(nr):                
                tempdis.append(999)
                for x in range(30):
                    if round(cur[i] + pred[i]) + checkx(i,x,nr) >= 2:
                        if tempdis[rout] > dis[i][x]:
                            if x not in t:
                                if cur[x] != 2:
                                    t[rout] = x
                                    tempdis[rout] = dis[i][x]
                if(t[rout]==-1):
                    continue
                message.append("from %d - > to %d, "%(rental[t[rout]],rental[i]))
                if cur[t[rout]] + round(cur[i] + pred[i]-2)>=2:
                    cur[t[rout]] = cur[t[rout]] + round(cur[i] + pred[i]-2)
                else:

                    cur[t[rout]] = 2
                message.append("move %d bikes"%(-round(cur[i] + pred[i]-2)))
            

    #print(cur)
    return t
    
def check(i,n):
    if round(cur[i]+pred[i])+maxsum(n)>=2:
        return True
    else:
        return False
        
def maxsum(n):
    total = 0
    predt = pred[:]
    for j in range(n):
        predtnp = np.array(predt)
        p = np.argmax(predtnp)
        total = total+round(predt[p]+cur[p]-5)
        predt.remove(max(predt))
    return total

def checkx(i,x,n):
    predt = pred[:]
    total = 0
    
    if n == 1:
        return round(pred[x] + cur[x] - 5)
    else:
        total = 0
        for j in range(n-1):
            predtnp = np.array(predt)
            p = np.argmax(predtnp)
            total = total+round(predt[p]+cur[p]-5)
            predt.remove(max(predt)) 
        return total+round(pred[x] + cur[x] - 5)

#print(b)
q=route()
tmessage = []
finalmessage = ""
for i in range(int(len(message)/2)):
    tmessage.append(message[i*2]+'   '+message[i*2+1])
#print(tmessage)

for i in range(len(tmessage)):
    finalmessage = finalmessage + tmessage[i] +"\n"
print(finalmessage)