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

# sys.path.append(r'C:\Users\romaa\Anaconda3\xgboost')
#print(sys.argv[1]); # 162. 대여소번호

num1 = np.array([221, 342, 568, 216, 316, 210, 340, 326, 106, 259,
                   302, 639, 540, 341, 212, 222, 336, 116, 124, 385,
                   247, 162, 329, 118, 128, 346, 907, 144, 529, 501])
num1 = np.sort(num1)
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
#     print(data_json)
    parsed_json = data_json['rentBikeStatus']['row']
#    print(parsed_json)
    
    k=0
    # print(parsed_json)
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

for key in a.keys():
    print(a[key])