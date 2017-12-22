# coding: utf-8

import time

def get_time(format='%Y-%m-%d %H:%M:%S'):
    return time.strftime(format, time.localtime(time.time()))


TOUZHU_JSON_DATA = 'touzhu_json_data'


POSITON_FIFTH = 'fifth'
POSTION_FOURTH = 'fourth'
POSTION_THIRD = 'third'
POSTION_SECOND = 'second'
POSTION_FIRST = 'first'


POSITON_FIFTH_ODDS = '5'
POSTION_FOURTH_ODDS = '4'
POSTION_THIRD_ODDS = '3'
POSTION_SECOND_ODDS = '2'
POSTION_FIRST_ODDS = '1'


XIAZHU_CODE_TYPE_DA = 'da'
XIAZHU_CODE_TYPE_XIAO = 'xiao'
XIAZHU_CODE_TYPE_DAN = 'dan'
XIAZHU_CODE_TYPE_SHUANG = 'shuang'
XIAZHU_CODE_TYPE_ZHI = 'zhi'
XIAZHU_CODE_TYPE_HE = 'he'


XIAZHU_CODE_MONEY_KEY = 'money'
XIAZHU_CODE_TYPE_KEY = 'property'

# 最低下注金额
DEFAULT_XIAZHU_MONKEY = 2

# SWITCH_XIAZHU_TYPE_FILE = 'switch_xiazhu_type_cn.json'
SWITCH_XIAZHU_TYPE_FILE = 'switch_xiazhu_type_en.json'
PEILV_FORMAT_FILE = 'peilv_format.json'
PROPERTY_CODE_FILE = '.code.json'
DEFAULT_PEILV_FILE = 'default_peilv.json'
TIME_PERIODS_MAP_FILE = 'time_periods_map.json'

# 获取时时彩投注号码接口
BET_CODE_URL = 'http://112.74.193.112:8080/test/PredictionResultServlet?period='

# 下注接口
XIAZHU_URL = 'https://ts111c.storei.net/game/ajax/wagers/AddAnyTime.aspx'

# 获取资源接口
GET_DATA_URL = 'https://nsb5.wf77.net/game/ajax/OutputIOContext.aspx'


# 24: 重庆时时彩
# 26: 天津时时彩
# 27: 新疆
# 23: 上海
# 29: 台湾4星彩
gType = 24


# 197: 双面盘
# 186: 一星定位
lType=197


GAME_CLOSE_STATUS = 'Msg_GameClose'  # 投注通道关闭状态码
GAME_SUCCESS_STATUS = 'Msg_Success'  # 投注成功状态码
GAME_ODDFALSE_STATUS = "Msg_OddChg"  # 赔率错误状态码
GAME_SESSION_LOST_STATUS = 'Msg_Logout'  #session过期状态码
GAME_MONEY_LESS_STATUS = 'Msg_ScMin'  # 投注金额小于最低值状态码
GMAE_ACCOUNT_MONEY_LESS_STATUS = 'Msg_NoBalance'  # 账号金额不足状态码

COOKIE = 'si0otzzeh4p2lxa5hm3r2or1'


