#!/usr/bin/env python
# coding:utf-8

import time
import os
import sys
import json
import traceback

base_dir = os.path.dirname(os.path.abspath(__file__))
# json_dir = os.path.join(base_dir, 'json')
json_dir = './json'
sys.path.append(base_dir)
import settings
from config import TIME_PEIODS_MAP


def get_time(format='%Y-%m-%d %H:%M:%S'):
    return time.strftime(format, time.localtime(time.time()))


def pause():
    f = input("Enter 'Y' continue, 'N' exit:")
    if f.lower() == 'n':
        exit(-1)
    else:
        pass


class Periods(object):
    def __init__(self):
        self.hour = 0
        self.min = 0
        self.periods = ''

    def is_interval_10_minute(self):
        self.refresh_time()
        if (self.hour > 9 and self.hour < 22) or (self.hour==9 and self.min>=50):
            return True
        else:
            return False

    def is_sleep_time(self):
        self.refresh_time()
        if (self.hour>1 and self.hour<9) or (self.hour==1 and self.min >=50) or (self.hour==9 and self.min<50):
            return True
        else:
            return False

    def get_map(self):
        return TIME_PEIODS_MAP
        # with open(os.path.join(json_dir, settings.TIME_PERIODS_MAP_FILE), 'r') as f:
        #     return json.loads(f.read())

    def refresh_time(self):
        t = time.localtime()
        self.hour = t.tm_hour
        self.min = t.tm_min

    def get_today(self):
        return get_time(format="%Y%m%d")

    def get_periods(self):
        self.refresh_time()

        hour_key = str(self.hour)
        min_key = str(int(self.min/5)*5)
        if self.is_interval_10_minute():
            min_key = str(int(self.min/10)*10)

        periods_map = self.get_map()
        try:
            self.periods = self.get_today() + periods_map[hour_key][min_key]
            return self.periods
        except Exception as e:
            traceback.print_exc()
            print(str(self.hour) + " " + str(self.min))
            print(str(hour_key) + " " + str(min_key))
            return None


if __name__ == "__main__":
    pe = Periods()
    print(pe.get_periods())
