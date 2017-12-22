#!/usr/bin/env python
# coding:utf-8

import logging
import time
import traceback
import os

log_level = logging.DEBUG


def get_time(format='%Y-%m-%d %H:%M:%S'):
    return time.strftime(format, time.localtime(time.time()))
def creat_log_dir(path='./log'):
    try:
        os.mkdir(path)
    except Exception as e:
        # traceback.print_exc()
        pass
creat_log_dir()

def create_log():
    # 创建一个logger
    logger = logging.getLogger(str(__name__))

    # 日志级别 ：
    logger.setLevel(log_level)
    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler('./log/'+get_time(format='%Y%m%d%H%M%S')+'.log', mode="w")
    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()

    # 定义handler的输出格式
    formatter = logging.Formatter(
        '%(levelname)s %(asctime)s [%(funcName)s, line:%(lineno)d ] - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # 给logger添加handler
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


log = create_log()
