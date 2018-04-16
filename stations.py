#!/usr/bin/env python2
#-*- coding=utf-8 -*-

import requests
import json
import re
import sys 
import os
import ssl
import time

reload(sys) 
sys.setdefaultencoding('utf8')

ssl._create_default_https_context = ssl._create_unverified_context

# 禁用安全请求警告
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
disable_warnings(InsecureRequestWarning)

STATIONS_URL = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9046'

HEADERS = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36', 
            'Referer' : 'https://kyfw.12306.cn/otn/leftTicket/init',
            'Host' : 'kyfw.12306.cn'
          }

INFO_FILE = "stations.json"

def queryByNet():# {{{
    try:
        result = requests.get(STATIONS_URL, headers=HEADERS, verify=False)
        if result.status_code != 200:
            return None
        station_list = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', result.text);
        station = {}
        for k,v in station_list:
            station[k] = v;

        if not station:
            return None

        station['timestamp'] = time.time();
        return station
    except Exception as e:
        print(e)
        return None# }}}

def getStationInfo():# {{{
    if os.path.exists(INFO_FILE):
        with open(INFO_FILE, "r") as f:
            station = json.load(f, encoding='utf-8');
            if station and time.time() - station['timestamp'] < 10 * 24 * 3600:
                del station['timestamp']
                return station

    with open(INFO_FILE, "w") as f:
        station = queryByNet()
        if not station:
            return None

        json.dump(station, f, encoding='utf-8', indent=4, sort_keys=True, ensure_ascii=False)
        del station['timestamp']
        return station# }}}

if __name__ == "__main__":
    station = getStationInfo();
    print(json.dumps(station, encoding='utf-8', indent=4, sort_keys=True, ensure_ascii=False))
