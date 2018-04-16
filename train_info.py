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

TRAIN_URL = r"https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no={0}&from_station_telecode={1}&to_station_telecode={2}&depart_date={3}"

TRAIN_LIST_URL = r"https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={0}&leftTicketDTO.from_station={1}&leftTicketDTO.to_station={2}&purpose_codes=ADULT"

HEADERS = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36', 
            'Referer' : 'https://kyfw.12306.cn/otn/leftTicket/init',
            'Host' : 'kyfw.12306.cn'
          }


def getDateByTimestamp(timestamp = None):# {{{
    if not timestamp:
        timestamp = time.time()

    return time.strftime("%Y-%m-%d", time.localtime(time.time()))# }}}

def queryByTrainId(train_id, from_station_id, to_station_id, date = getDateByTimestamp(time.time())):# {{{
    if not all((train_id, from_station_id, to_station_id, date)):
        return None;
    
    try:
        url = TRAIN_URL.format(train_id, from_station_id, to_station_id, date);
        result = requests.get(url, headers=HEADERS, verify=False)
        if result.status_code != 200:
            print "queryByTrainid Error"
            return None;

        return result.json()['data']['data']
    except Exception as e:
        print e
        return None

    return None# }}}# }}}

def getByFile(file_name):# {{{
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            data = json.load(f, encoding='utf-8');
            if not data:
                return {}
            return data

    return {}# }}}

def saveToFile(file_name, data):# {{{
    if not all((file_name, data, isinstance(data, dict))):
        return False

    with open(file_name, "w") as f:
        json.dump(station, f, encoding='utf-8', indent=4, sort_keys=True, ensure_ascii=False)# }}}

def getTrainList(from_station, to_station, date, time_limit = None, durationi = None, by_list = True):# {{{
    if not all((from_station, to_station, date)):
        return None

    try:
        url = TRAIN_LIST_URL.format(date, from_station, to_station);
        result = requests.get(url, headers=HEADERS, verify=False)
        if result.status_code != 200:
            print "queryByTrainid Error"
            return None;

        train = []
        if not by_list:
            train = {}
        train_list = result.json()['data']['result']
        for raw_train in train_list:
            raw_train_list = raw_train.split('|')
            t = {'id' : raw_train_list[2], 'no': raw_train_list[3], 'start_station': raw_train_list[4], 'end_station':raw_train_list[5], 'require_start':raw_train_list[6], 'require_end':raw_train_list[7], 'start_time' : raw_train_list[8], 'end_time' : raw_train_list[9], 'duration' : raw_train_list[10], 'business_seat':raw_train_list[-5], 'first_seat':raw_train_list[-6], 'second_seat':raw_train_list[-7], 'hard_seat':raw_train_list[-8], 'no_seat':raw_train_list[-11], 'soft_berth':raw_train_list[-14], 'hard_berth':raw_train_list[-9]}

            if time_limit:
                times = time_limit.split('-')
                if t['start_time'] < times[0] or t['end_time'] > times[1]:
                    continue

            if by_list:
                train.append(t);
            else:
                train[t['no']] = t
    
        return train

    except Exception as e:
        print "ERROR!", e

    return None# }}}

if __name__ == "__main__":
    #print json.dumps(queryByTrainId('5l000G132141', 'AOH', 'NXG'), indent=4, encoding='utf-8', ensure_ascii=False)
    print json.dumps(getTrainList('SHH', 'NCG', '2018-01-29', "07:00-19:00", by_list=False), indent=4, encoding='utf-8', ensure_ascii=False)

