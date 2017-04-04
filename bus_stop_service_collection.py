import requests
import json

import time
from datetime import datetime, timezone, timedelta

import os

import multiprocessing as mp


headers = {
    'AccountKey': 'J4mwYTb4FKiNkWpDHLapZQ==',
    'accept': 'application/json'
}

#http://datamall2.mytransport.sg/ltaodataservice/BusArrival?BusStopID=83139&SST=True
url = 'http://datamall2.mytransport.sg/ltaodataservice/BusArrival?' #Resource URL

datetime_fmt =  '%Y%m%d_%H%M%S'
timezone_sg = timezone(timedelta(hours=+8))
data_path = 'busstop_data/'

bus_stop_static_data = 'static/stops_040217.json'


def load_bus_stop():
    with open(bus_stop_static_data) as json_data:
        temp = json.load(json_data)
    skip = set(['Non Stop','Express'])

    bus_stop_master = []
    for stop in temp:
        if stop['Longitude'] == 0 or stop['Latitude'] == 0:
            continue
        if stop['Description'] in skip:
            continue
        bus_stop_master.append(stop)

    return bus_stop_master

def collect_one_stop(stop_code):
    query_url = '{}BusStopID={}&SST=True'.format(url, stop_code)
    res = requests.get(query_url, headers=headers).json()
    return res

def collect_data(bus_stop_master, index=[]):
    pool = mp.Pool(processes=8)
    
    stop_code_list = [S['BusStopCode'] for S in bus_stop_master]
    iter_count = 0

    while True:
        time_start = datetime.now(timezone_sg).strftime(datetime_fmt)
        res_list = pool.map(collect_one_stop, stop_code_list)   
        time_end = datetime.now(timezone_sg).strftime(datetime_fmt)
        iter_count+=1
        print('complete {} round. Start:{} End:{}'.format(iter_count, time_start, time_end))
        #timestamp
        out_fn = '{}{}_{}.txt'.format(data_path ,time_start, time_end)
        with open(out_fn,'w') as F:
            F.write(json.dumps(res_list))

        
        # to sleep during night time in SG 2-5am
        time_now = datetime.now(timezone_sg)
        if time_now.hour < 5 and time_now.hour>=2:
            print('Sleep @ ',time_now)
            time_5am = datetime(time_now.year,time_now.month,time_now.day,5,0)
            time.sleep((time_5am-time_now).seconds)
            print('Wake @ ', datetime.now(timezone_sg))
        else:
            # nap for 5 mins
            time.sleep(60*5)



if __name__ == '__main__':
    master = load_bus_stop()
    collect_data(master)

