import math
from posixpath import split
import requests
from bs4 import BeautifulSoup
import json
import re
import math
import sys
import time, datetime
import csv

import numpy as np
import pandas as pd
import seaborn as sns
import timeit
import collections
from dataclasses import dataclass
from typing import NamedTuple

#
#   startStr부터 ~ endStr 사이의 문자열 반환
#
def getStrBetweenAnB(fullStr, startStr, endStr):
    startStrLen = len(startStr)    

    # find start index
    startIdx = fullStr.find(startStr) + startStrLen

    # find end index
    endIdx = fullStr.find(endStr, startIdx)

    return fullStr[startIdx:endIdx]

#
#    Get Response
#
def getRes(url, headers):
    res = requests.get(url, headers = headers)
    time.sleep(1)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
        
    return res

#
#    해당 층수 리턴.  
#
def getFloorInfo(floorInfo):
    result = floorInfo.split('/')
    return str(result[0])

#
#    string으로 저장된 가격을 int 값으로 변경하여 반환.
#
def getPriceInfo(price):
    list = price.split('억 ')
    result = 0
    
    if len(list) is 2: # ex) 3억 6,000
        
        result = int(list[0]) * 10000 + int(list[1].replace(',', ''))
    else: # ex) 3억
        result = int(list[0].replace('억','0000')) * 10000
        
    return int(result)


#
#    real estate struct
#
class RealEstateInfo(NamedTuple):
    name:str
    spc1:float
    spc2:float
    priceInfo:int
    floorInfo:str

        
#
#       Main
#
keyword = "원주시 무실동"

url = "https://m.land.naver.com/search/result/" + keyword
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}

resArea = getRes(url, headers)

strResult = getStrBetweenAnB(resArea.text, "filter: {", "},")

"""
f = open("D:/newInfo.txt", 'w', encoding='utf-8')
f.write(strResult)
f.close()
"""

lat = getStrBetweenAnB(strResult, "lat: '","',")
lon = getStrBetweenAnB(strResult, "lon: '","',")
z = getStrBetweenAnB(strResult, "z: '","',")
cortarNo = getStrBetweenAnB(strResult, "cortarNo: '","',")
searchType = "APT"

rletTpCds = getStrBetweenAnB(strResult, "rletTpCds: '","',")
tradTpCds = getStrBetweenAnB(strResult, "tradTpCds: '","',")

# 지도에서 단지들 url
onMapURL = f"https://m.land.naver.com/cluster/clusterList?cortarNo={cortarNo}&rletTpCd={searchType}&tradTpCd=A1%3AB1%3AB2&z={z}&lat={lat}&lon={lon}&btm=37.4756089&lft=127.099033&addon=COMPLEX&bAddon=COMPLEX&isOnlyIsale=false"

resMap = getRes(onMapURL, headers)

mapJsonObject = json.loads(resMap.text)
mapArray = mapJsonObject["data"]["COMPLEX"]

# 매물 정보
for val in mapArray:
    print(f'{val["lgeo"]}, {val["lat"]}, {val["lon"]}, {val["count"]}')
    
    # 매물 url
    ipage = int(int(val['count'])/20 + 2)
    
    # 각 지도에서 20개의 매물이 합쳐져 보이는거 체크.
    for pageCnt in range(1, ipage):
        # 매물 20개가 넘는 위치들 카운트 하기 위함.
        offeringsURL = f"https://m.land.naver.com/cluster/ajax/complexList?itemId={val['lgeo']}&lgeo={val['lgeo']}&rletTpCd=APT&tradTpCd=A1:B1:B2&z={z}&lat={val['lat']}&lon={val['lon']}&btm=37.4404697&lft=127.1156627&top=37.5303033&rgt=127.1285373&cortarNo={cortarNo}&isOnlyIsale=false&sort=readRank&page={pageCnt}"
        resOfferings = getRes(offeringsURL, headers)

        offeringsJsonObject = json.loads(resOfferings.text)
        offeringsArray = offeringsJsonObject["result"]

        # 지역 전체 매물 array
        for v in offeringsArray:
            if int(v['totHsehCnt']) > 300:
                print(f"{v['hscpNm']}, {v['dealCnt']}, {v['leaseCnt']}")

                # 아파트 매물 url
                num = int(v['dealCnt']) + int(v['leaseCnt'])
                aptPage = int(num / 20) + 2
                
                # apt 매물 갯수가 20개 이하인 경우.
                
                myDealList = []
                myLeaseList = []
                
                # 매매, 전세 페이지 처리. # 20개 이상일 때 page 증가됨.
                for aptCnt in range(1, aptPage):
                    print(f"page count : {aptCnt}")
                    aptUrl = f'https://m.land.naver.com/complex/getComplexArticleList?hscpNo={v["hscpNo"]}&cortarNo=1171010800&tradTpCd=A1:B1&order=point_&showR0=N&page={aptCnt}'
                    resApt = getRes(aptUrl, headers)
                    
                    aptJsonObject = json.loads(resApt.text)
                    aptArray = aptJsonObject['result']['list']
                    
                    # 매매, 전세 데이터 저장 list
                    
                    
                    # APT 단지 매물 검색
                    for apts in aptArray:
                        #print(f"{apts['atclNm']}, {apts['tradTpNm']}, {apts['prcInfo']}")
                        
                        floorInfo = getFloorInfo(apts['flrInfo'])
                        priceInfo = getPriceInfo(apts['prcInfo'])
                        
                        # 층수 "flrInfo":"11/15" "저/15", "고/15"
                        # 공급/전용 "spc1":"103.12","spc2":"84.7"
                        if apts['tradTpNm'] == "매매":
                            if floorInfo == "저":
                                continue
                            elif  floorInfo == '중' or floorInfo == '고':
                                myDealList.append(RealEstateInfo(f"{apts['atclNm']}", float(apts['spc1']), float(apts['spc2']), priceInfo, f"{floorInfo}"))                                        
                                continue
                            elif int(floorInfo) < 5:
                                continue
                            else:
                                myDealList.append(RealEstateInfo(f"{apts['atclNm']}", float(apts['spc1']), float(apts['spc2']), priceInfo, f"{floorInfo}"))     
                            
                            
                        elif apts['tradTpNm'] == "전세":
                            if floorInfo == "저":
                                continue
                            elif  floorInfo == '중' or floorInfo == '고':
                                myDealList.append(RealEstateInfo(f"{apts['atclNm']}", float(apts['spc1']), float(apts['spc2']), priceInfo, f"{apts['flrInfo']}"))                                        
                                continue
                            elif int(floorInfo) < 5:
                                continue
                            else:
                                myDealList.append(RealEstateInfo(f"{apts['atclNm']}", float(apts['spc1']), float(apts['spc2']), priceInfo, f"{apts['flrInfo']}"))     
                            
                        
                        #
                        # 구조체로 단지이름, 전용면적, 매매or전세 이 세가지로 key를 가지며 구분,
                        # 엑셀 시트에 추가할 때 저 3가지면 고유값을 가질 수 있음.
                        # 해당 list에서 저층 제외로 sort. 매매가는 가장 낮은 가격 - 전세는 중간값으로
                        #
                        
                        """
                        # real estate info.
                            class RealEstateInfo(NamedTuple):
                                name:str
                                spc1:float
                                spc2:float
                                priceInfo:str
                                floorInfo:str
                        """
                        
                myDealList.sort()
                for val in range(0, len(myDealList)):
                    print(f"{myDealList[val]}")
                        
                        
                        

                    
                        