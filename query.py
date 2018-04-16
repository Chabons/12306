#!/usr/bin/python3
#-*- coding=utf-8 -*-

import requests
import os
import json
import time
import re
import ssl
from stations import getStationInfo

import sys 
reload(sys) 
sys.setdefaultencoding('utf8')

ssl._create_default_https_context = ssl._create_unverified_context

# 禁用安全请求警告
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
disable_warnings(InsecureRequestWarning)

from stations import getStationInfo
from train_info import *

TRAIN_DATE = '2018-02-12'
FROM_STATION = "上海虹桥".decode("utf-8")
TO_STATION = "南昌西".decode("utf-8")
TRAINS_FILE = "train_info.json"
TIME_LIMIT = "07:00-19:00"

STATION_NAME = getStationInfo()
TRAIN_INFO = getByFile(TRAINS_FILE)

TRAIN_LIST = getTrainList(STATION_NAME[FROM_STATION], STATION_NAME[TO_STATION], TRAIN_DATE, TIME_LIMIT)
#print json.dumps(TRAIN_LIST, indent=4, encoding='utf-8', ensure_ascii=False)
#exit()

SEAT_TYPE = ('no_seat', 'first_seat', 'second_seat', 'hard_seat', 'hard_berth')

#train_no no_seat second_seat first_seat hard_seat hard_berth

def trainInfoPrint(train):
    for ks in SEAT_TYPE:
        if not train[ks] or train[ks] == '无':
            print "no:%s no ticket" %train['no']
            return;

    print "{0} no_seat:{1} second_seat:{2} first_seat:{3} hard_seat{4} hard_berth{5}".format("{0} {1}->{2}".format(train['no'], train['start_station'], train['end_station']),
        train['no_seat'], train['second_seat'], train['first_seat'], train['hard_seat'],
        train['hard_berth'])

se = requests.session()
se.verify = False

def getTrainInfo(train):
    if TRAIN_INFO.has_key(train['no']):
        return TRAIN_INFO[train_no]

    info = queryByTrainId(train['id'], train['require_start'], train['require_end'])
    if not info:
        print "query no:%s error" %train['no']
        return None

    return info

def query():
    for k in TRAIN_LIST:
        trainInfoPrint(k)

        print "loop for train_list"
        info = getTrainInfo(k)
        if not info:
            continue

        find = False
        for i in info:
            if not find and i['station_name'] != FROM_STATION:
                continue
            find = True
            if i['station_name'] == FROM_STATION:
                continue

            print k['no'], FROM_STATION, i['station_name']

            train_map = getTrainList(STATION_NAME[FROM_STATION], STATION_NAME[i['station_name'].decode('utf-8')], TRAIN_DATE, by_list=False)
            #print json.dumps(train_map, indent=4, encoding='utf-8', ensure_ascii=False)
            print "loop2 ---------------------------"
            if train_map and train_map.has_key(k['no']):
                trainInfoPrint(train_map[k['no']])

            if i['station_name'] == TO_STATION:
                break

while True:
    query()
    time.sleep(1)
