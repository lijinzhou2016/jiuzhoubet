#!/usr/bin/env python
# coding:utf-8

import os
import random
import sys
import traceback

import requests
import json
import time
from time import strftime

base_dir = os.path.dirname(os.path.abspath(__file__))
# json_dir = os.path.join(base_dir, 'json')
json_dir = '.'
sys.path.append(base_dir)
from mylogger import log
import settings
from util import Periods
from get_xiazhu_haoma import ProductCodes
import util
from myuuid import authour
from config import DEFAULT_ODDS, ODDS_FORMAT, TOUZHU_TYPE_ENCODE
from sendermsg import reader_phone, Phone, Sender
import sendermsg

phone=''

ph_list = reader_phone()
if not ph_list:
    print(u"请在当前了目录配置phone.txt")
    print(u"配置完成后重启应用")
    time.sleep(5)
    exit(-1)
ph_obj = Phone()

def send_msg(msg):
    for ph in ph_list:
        sender = Sender(ph)
        sender.send(msg)
        time.sleep(3)

def get_time(format='%Y-%m-%d %H:%M:%S'):
    return time.strftime(format, time.localtime(time.time()))

def get_session():
    try:
        if os.path.exists('./.session.txt'):
            with open('./.session.txt', 'r') as f:
                return f.read()
        return ""
    except Exception as e:
        print(traceback.print_exc())
        return ""


def save_session_to_file(session):
    try:
        with open('./.session.txt', 'w') as f:
            f.write(session)
    except Exception as e:
        print(traceback.print_exc())

class Bets(object):

    def __init__(self, log=log, lType=197, kType=197, gType=24, post_url=settings.GET_DATA_URL):

        self._cookie = 'ASP.NET_SessionId='+get_session()
        self._headers = {'Cookie': self._cookie}
        self._lType = lType
        self._kType = kType
        self._gType = gType
        self._logger = log
        self._post_url = post_url

    def get_time(self, format='%Y-%m-%d %H:%M:%S'):
        return strftime(format, time.localtime(time.time()))

    def format_post_time(self):
        return "GMT+8 "+str(self.get_time())

    def _post(self, url, headers, data, timeout=15):
        '''发送post请求

        :param url:
        :param headers:
        :param data:
        :param timeout:
        :return: 响应body
        '''
        try:
            rs = requests.post(url, headers=headers, data=data, timeout=timeout)
            if rs.status_code == 200:
                data = rs.text
                return data

            else:
                self._logger.error("Response code: "+str(rs.status_code))
                # send_msg(sendermsg.MSG_502_ERROR)  # 短信通知， 502错误
                if rs.status_code == 502:
                    return json.dumps({"status": "502"})
                return None
        except Exception as e:
            self._logger.error(str(e))
            return None

    def get_default_peilv_map(self):
        '''获取默认赔率

        获取实时赔率失败时，可以试一下此赔率
        :return:
        '''
        return DEFAULT_ODDS
        # with open(os.path.join(json_dir, settings.DEFAULT_PEILV_FILE)) as f:
        #     return json.loads(f.read())

    def get_peilv_format_map(self):
        '''读取赔率封装格式表，并返回

        :return:
        '''
        return ODDS_FORMAT
        # with open(os.path.join(json_dir, settings.PEILV_FORMAT_FILE)) as f:
        #     return json.loads(f.read())

    def get_switch_xiazhu_type_map(self):
        '''读取下注号码转换成post格式的转换表，并返回

        :return:
        '''
        return TOUZHU_TYPE_ENCODE
        # with open(os.path.join(json_dir, settings.SWITCH_XIAZHU_TYPE_FILE)) as f:
        #     return json.loads(f.read())

    def get_peilv(self, game_type='197'):

        '''获取赔率

            52: 小
            51: 大
            53: 单
            54: 双
            11: 质
            12: 合

            猜想：
            1: 个位
            5: 万位

        :return: {'111': 1.99, '112': 1.99, '151': 1.99, '152': 1.99, '153': 1.99, '154': 1.99,
                  '211': 1.99, '212': 1.99, '251': 1.99, '252': 1.99, '253': 1.99, '254': 1.99,
                  '311': 1.99, '312': 1.99, '351': 1.99, '352': 1.99, '353': 1.99, '354': 1.99,
                  '411': 1.99, '412': 1.99, '451': 1.99, '452': 1.99, '453': 1.99, '454': 1.99,
                  '511': 1.99, '512': 1.99, '551': 1.99, '552': 1.99, '553': 1.99, '554': 1.99}
        '''

        data = {
            'gType': self._gType,
            'dataType': 'floatodds'
        }
        rs = self._post(self._post_url, self.get_headers(), data)
        try:
            if 'status' in rs:
                if json.loads(rs)['status'] == settings.GAME_SESSION_LOST_STATUS:
                    return None
            if rs:
                return json.loads(rs)['floatOdds'][game_type]
            else:
                return None
        except Exception as e:
            log.error("get Odds: "+str(e))
            return None

    def set_headers(self):  # 设置headers
        self._headers = {'Cookie': self._cookie,
                         "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
                         }

    def get_headers(self):  # 获取headers
        return self._headers

    def set_cookie(self):  # 获取时时彩网站登录session
        session_id = str(input('请输入session:')).strip()
        save_session_to_file(session_id)
        self._cookie = 'ASP.NET_SessionId' \
                       '=' + session_id
        self.set_headers()
        # print(self._headers)

    def test_cookie(self):
        return self.get_peilv()

    def send_msg(self, msg=''):
        print('发短信 '+ str(msg))

    def get_money(self):
        # {"balance": 274.4400}

        data = {"dataType": "UB"}
        url = settings.REQUESTS_MONEY_URL
        try:
            rs = requests.post(url, data=data, headers=self.get_headers(), timeout=10)
            if rs.status_code == 200:
                return float(rs.json()['balance'])
            else:
                print("requests money status code "+str(rs.status_code))
                return None
        except Exception as e:
            print(e)
            return None

    def get_qishu(self):
        '''
            获取投注期数

            :return: {"gid":20171203107,"gameStatus":1,"overMinute":10,"endDate":12,"isEnd":false}
        '''

        data = {
            'gType':self._gType,
            'dataType':'status'
        }
        rs = self._post(self._post_url, self.get_headers(), data)
        try:
            if rs:
                return json.loads(rs)['game']['24']
            else:
                return None
        except Exception as e:
            log.error("get gid: " + str(e))
            return None

    def get_result(self, qishu=None):
        '''获取历史中奖结果

            :return: 若传入具体期数，则直接返回该期数的中奖号码，否则返回如下字典

                    {'A20171204047': {'num': '06632'},
                     'A20171204046': {'num': '47907'},
                      ...
                    }
        '''

        data = {
            'gType': self._gType,
            'dataType': 'resultinfo'
        }
        rs = self._post(self._gType, self.get_headers(), data)
        if rs:
            history = json.loads(rs)['history']
            if qishu:
                if qishu in history:
                    qishu = "A" + qishu
                    return history[qishu]['num']
                else:
                    print(qishu+' No result')
                    return None

            return json.loads(rs)['history']
        else:
            return None

    def get_propery_code_data(self):
        '''读取下注号码json文件，并返回文件内容

        :return:
        '''
        try:
            # data = json.loads(os.environ.pop(settings.TOUZHU_JSON_DATA))
            # return data
            with open(os.path.join(json_dir, settings.PROPERTY_CODE_FILE), 'r') as f:
                return json.loads(f.read())
        except Exception as e:
            traceback.print_exc()
            self._logger.error("get json data error")
            return None

    def format_24_197_post_data(self, code_data, peilv_data, gid, amt):
        '''

        :return:
        '''
        fifth = []
        fourth = []
        third = []
        second = []
        first = []

        fifth_name = []
        fourth_name = []
        third_name = []
        second_name = []
        first_name = []

        fifth_odds = []
        fourth_odds = []
        third_odds = []
        second_odds = []
        first_odds = []

        encode_switch_map = self.get_switch_xiazhu_type_map()

        for data in code_data[settings.POSITON_FIFTH]:  # 万位投注号码列表
            if data[settings.XIAZHU_CODE_MONEY_KEY] == amt:
                fifth.append(encode_switch_map[data[settings.XIAZHU_CODE_TYPE_KEY]])
                fifth_name.append(data[settings.XIAZHU_CODE_TYPE_KEY])

        for data in code_data[settings.POSTION_FOURTH]:  # 千位投注号码列表
            if data[settings.XIAZHU_CODE_MONEY_KEY] == amt:
                fourth.append(encode_switch_map[data[settings.XIAZHU_CODE_TYPE_KEY]])
                fourth_name.append(data[settings.XIAZHU_CODE_TYPE_KEY])

        for data in code_data[settings.POSTION_THIRD]:  # 百位投注号码列表
            if data[settings.XIAZHU_CODE_MONEY_KEY] == amt:
                third.append(encode_switch_map[data[settings.XIAZHU_CODE_TYPE_KEY]])
                third_name.append(data[settings.XIAZHU_CODE_TYPE_KEY])

        for data in code_data[settings.POSTION_SECOND]:  # 十位投注号码列表
            if data[settings.XIAZHU_CODE_MONEY_KEY] == amt:
                second.append(encode_switch_map[data[settings.XIAZHU_CODE_TYPE_KEY]])
                second_name.append(data[settings.XIAZHU_CODE_TYPE_KEY])

        for data in code_data[settings.POSTION_FIRST]:  # 个位投注号码列表
            if data[settings.XIAZHU_CODE_MONEY_KEY] == amt:
                first.append(encode_switch_map[data[settings.XIAZHU_CODE_TYPE_KEY]])
                first_name.append(data[settings.XIAZHU_CODE_TYPE_KEY])

        for num in fifth:  # 万位投注号码赔率
            fifth_odds.append(str(peilv_data[settings.POSITON_FIFTH_ODDS + num]))

        for num in fourth:  # 千位投注号码赔率
            fourth_odds.append(str(peilv_data[settings.POSITON_FIFTH_ODDS + num]))

        for num in third:  # 百位投注号码赔率
            third_odds.append(str(peilv_data[settings.POSITON_FIFTH_ODDS + num]))

        for num in second:  # 十位投注号码赔率
            second_odds.append(str(peilv_data[settings.POSITON_FIFTH_ODDS + num]))

        for num in first:  # 个位投注号码赔率
            first_odds.append(str(peilv_data[settings.POSITON_FIFTH_ODDS + num]))

        # print(fifth)
        # print(fifth_odds)
        # print(fourth)
        # print(fourth_odds)
        # print(third)
        # print(third_odds)
        # print(second)
        # print(second_odds)
        # print(first)
        # print(first_odds)



        bType = ';'.join([','.join(fifth),
                         ','.join(fourth),
                         ','.join(third),
                         ','.join(second),
                         ','.join(first)])

        wOdds = ';'.join([','.join(fifth_odds),
                         ','.join(fourth_odds),
                         ','.join(third_odds),
                         ','.join(second_odds),
                         ','.join(first_odds)])

        bType_name = ';'.join([','.join(fifth_name),
                         ','.join(fourth_name),
                         ','.join(third_name),
                         ','.join(second_name),
                         ','.join(first_name)])

        log_info = bType_name + " " + str(amt)
        log.info(log_info)

        data = {
            "gid": gid,
            "gType": self._gType,
            "kType": self._kType,
            "lType": self._lType,
            "spType": "oneStar",
            "count": 1,
            "delGid": "",
            "bType": bType,
            "wOdds": wOdds,
            "amt": amt,
            "betTime": self.format_post_time()
        }

        return {'betData': str(data)}

    def xiadan(self, code_data, gid, amt):
        ''' 投注

        :return: 响应json

        '''
        log.info(gid)
        peilv_data = self.get_peilv()
        if peilv_data is None:
            peilv_data = self.get_default_peilv_map()
        post_data = self.format_24_197_post_data(code_data, peilv_data, gid, amt)
        post_url = settings.XIAZHU_URL
        # print(post_data)
        post_headers=self.get_headers()
        # time.sleep(3)
        return self._post(post_url, data=post_data, headers=post_headers)


class Delay(object):
    def __init__(self):
        self._display_flag = True

    def disable_display(self):
        self._display_flag = False

    def enable_display(self):
        self._display_flag = True

    def delay(self, t):
        tt = range(t)
        tt = list(tt)
        tt.reverse()
        for tp in tt:
            print("\r" + "Total Delay: " + str(t) + "  " + "Leave: " + str(tp) + "  ", end="")
            time.sleep(1)
        print()

    def random_delay(self, start=1, stop=5):
        t = random.randint(start, stop)
        self.delay(t)

    def loop_display_time(self, note=""):
        while self._display_flag:
            self.display_time(note=note)

    def display_time(self, note=""):
        t = get_time()
        print('\r' + t + note, end="")
        time.sleep(1)


if __name__ == "__main__":
    delay = Delay()
    # if not authour():
    #     print(u"此电脑没有授权")
    #     delay.delay(10)
    #     exit(-1)

    bets = Bets()
    period = Periods()


    gid = period.get_periods()
    before_gid = 0

    from users import Users
    user = Users()
    if not user.check_user():
        print("此账号不存在")
        time.sleep(3)
        exit(-1)
    phone = user.get_phone()
    product = ProductCodes()
    for i in range(3):
        if bets.test_cookie() is None:
            bets.set_cookie()
        else:
            break
        if i == 2:
            exit(-1)

    yuanshi_money=""
    for i in range(3):
        yuanshi_money = bets.get_money()
        if yuanshi_money:
            send_msg("开始："+str(yuanshi_money))
            break
        time.sleep(3)

    while True:

        while period.is_sleep_time():  # 1：55 ~ 9：50 之间，等待
            delay.display_time()
        print()

        while int(gid) == int(before_gid):  # 等待进入新的一期购买时间
            delay.display_time("   wait " + str(int(gid)+1))
            gid = period.get_periods()  # 获取当前期数

        if period.get_msg_note_time():
            for i in range(3):
                money = bets.get_money()
                if money:
                    send_msg(str(money-yuanshi_money))
                    break
                time.sleep(3)


        # 根据投注时间间隔不同进行不同的延时
        if int(gid) > int(before_gid):
            print()
            if int(before_gid) == 0:
                before_gid = gid
            else:
                before_gid = gid
                if period.is_interval_10_minute():  # 若10分钟一期，延时2-3分钟购买
                    delay.random_delay(120, 180)
                else:       # 若5分钟一期，延时1分钟购买
                    delay.delay(60)

        # 获取发号服务器的下注号码并保存到文件
        print("begin to request bet code ...")
        REQUESTS_TIMES = 12
        for t in range(REQUESTS_TIMES):
            status = product.save_current_json(str(gid))
            if status:  # 请求发号器接口成功
                # 读取保存下来的下注号码
                code_data = bets.get_propery_code_data()
                if code_data.get("hasDate"):
                    if code_data['period'] != str(gid):  # 期数不相等
                        delay.delay(10)
                        continue
                    print("request code success")
                    break
                else:
                    if t == REQUESTS_TIMES - 1:
                        send_msg(sendermsg.MSG_REQUESTS_CODE_ERROR)
                        break
                    delay.delay(10)
                    continue
            else:  # 请求发号器接口失败
                print(u"请求发号器接口失败")
                send_msg(str(gid)[-3:]+":"+"请求FHQ接口失败")
                delay.delay(10)

        # code_data = bets.get_propery_code_data()
        if not code_data["isbet"]:
            log.info(str(gid)+" Not buy")
            continue


        amt_list = code_data[settings.XIAZHU_CODE_MONEY_KEY]
        for amt in amt_list:
            for i in range(3):
                money = bets.get_money()
                if money:
                    log.info("Before Bet Money: " + str(money))
                    break
                if i == 2:
                    log.error("Get Money Failed")
                time.sleep(3)

            for loop in range(4):
                try:
                    rs = bets.xiadan(code_data, gid, amt)
                    if rs is None:
                        send_msg(str(gid)[-3:]+":"+sendermsg.MSG_REQUESTS_BET_OVER)
                        log.error('Bet Server No Response')
                        delay.random_delay(5, 10)
                        continue
                    if json.loads(rs)['status'] == settings.GAME_SUCCESS_STATUS:
                        log.info("Bet Success")
                        break
                    if json.loads(rs)['status'] == settings.GAME_CLOSE_STATUS:
                        send_msg(str(gid)[-3:]+":"+sendermsg.MSG_GAME_OVER)
                        log.error('Game Over')
                        break
                    if json.loads(rs)['status'] == settings.GAME_SESSION_LOST_STATUS:
                        send_msg(str(gid)[-3:]+":"+sendermsg.MSG_SESSION_OVER)
                        log.error("Session over time")
                        bets.set_cookie()
                        continue
                    if json.loads(rs)['status'] == settings.GAME_MONEY_LESS_STATUS:
                        log.error("Touzhu Money less")
                        break
                    if json.loads(rs)['status'] == settings.GAME_ODD_FALSE_STATUS:
                        send_msg(str(gid)[-3:]+":"+sendermsg.MSG_ODD_ERROR)
                        log.error("Odds exchange")
                        delay.random_delay(5, 10)
                        continue
                    if json.loads(rs)['status'] == settings.GMAE_ACCOUNT_MONEY_LESS_STATUS:
                        send_msg(str(gid)[-3:] + ":" + sendermsg.MSG_ACCOUNT_LESS)
                        log.error("Your account has not enough money")
                        util.pause()
                        break
                    if json.loads(rs)['status'] == "502":
                        f = True
                        for i in range(3): # 获取三次金额，保证正确率
                            m = bets.get_money()
                            if m:
                                break
                            if i == 2:
                                f = False
                                m=None
                            time.sleep(3)

                        if m:
                            if m < money or money > m:
                                log.info("Bet Success")
                                break

                        if not m:
                            if loop == 3:
                                send_msg(str(gid)[-3:] + ":" + sendermsg.MSG_502_ERROR)
                                log.error("502 error")

                except Exception as e:
                    log.error(str(traceback.print_exc()))
                    continue

            for i in range(3):
                time.sleep(5)
                money = bets.get_money()
                if money:
                    log.info("After Bet Money: " + str(money))
                    break
                time.sleep(3)

