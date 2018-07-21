# -*- coding: utf-8 -*-
from urllib import parse
import hashlib
import requests
import json
from PIL import Image
import matplotlib.pyplot as plt
from io import BytesIO


def getPoiInfo(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(e)


def parsePoiLatLng(jsonData):
    jsonData = json.loads(jsonData)
    if 'result' in jsonData.keys():
        if 'location' in jsonData.get('result'):
            lng = jsonData.get('result').get('location').get('lng')
            lat = jsonData.get('result').get('location').get('lat')
        return lng,lat


def getBaiDuPanorama(AK,lng,lat):
    url = 'http://api.map.baidu.com/panorama/v2?ak=%s&width=512&height=256&location=%s,%s&fov=360'%(AK,lng,lat)
    try:
        response = requests.get(url)
        if response.status_code==200:
            return response.content
        return None
    except Exception as e:
        print('获取全景图出错', e)


if __name__=='__main__':

    query_POI = '深圳大学西门'
    # 创建应用后选择以sn校验方式，会有AK和SK
    AK = '你的AK'
    SK = '你的SK'

    queryStr = '/geocoder/v2/?address=%s&output=json&ak=%s' % (query_POI, AK)
    encodedStr = parse.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")
    rawStr = encodedStr + '%s' % SK
    sn = hashlib.md5(parse.quote_plus(rawStr).encode('utf-8')).hexdigest()
    url = 'http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&ak=%s&sn=%s' % (query_POI, AK, sn)

    jsonData = getPoiInfo(url=url)
    print(jsonData)
    lng,lat = parsePoiLatLng(jsonData=jsonData)
    print('%s 经纬度 %s,%s'%(query_POI,lng,lat))
    #创建另外一个应用选择IP白名单校验的AK填在下面
    AK2 = '你的另一个AK'
    pic = getBaiDuPanorama(AK=AK2, lng=lng, lat=lat)
    pic = Image.open(BytesIO(pic))
    plt.imshow(pic)
    plt.show()

