import requests
import time

def get_time(format='%Y-%m-%d %H:%M:%S'):
    return time.strftime(format, time.localtime(time.time()))

def post_data():
    data = {
        "gid": 20171226003,
        "gType": 24,
        "kType": 197,
        "lType": 197,
        "spType": "oneStar",
        "count": 1,
        "delGid": "",
        "bType": "53;;;;",
        "wOdds": "1.99;;;;",
        "amt": 2,
        "betTime": "GMT+8 " + get_time()
    }
    print(data)

    url = 'https://ts111c.storei.net/game/ajax/wagers/AddAnyTime.aspx'
    headers = {
        # "Accept":"application/json, text/javascript, */*; q=0.01",
        # "Accept-Encoding":"gzip, deflate, br",
        # "Accept-Language":"zh-CN,zh;q=0.9",
        # "Connection":"keep-alive",
        # "Content-Length":"335",
        # "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie":"ASP.NET_SessionId=0mmitghpkuy1zwaswae2hk21; c257685057-231435ic=c404942-125387-547401",
        # "Host":"nw111.cdn3168.net"
        # "Origin":"https://nw111.cdn3168.net",
        # "Referer":"https://nw111.cdn3168.net/game/aspx/anyTime/AnyTime.aspx",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
        # "X-Requested-With":"XMLHttpRequest"
        }
    post_data = {'betData': str(data)}

    rs = requests.post(url, data=post_data, headers=headers, timeout=5)
    print(rs.status_code)
    print(rs.text)


post_data()


def delay(t):
    tt = range(t)
    tt = list(tt)
    tt.reverse()
    for tp in tt:
        print("\r" + "Total Delay: " + str(t) + "  " + "Leave: " + str(tp), end="")
        time.sleep(1)


def get_time(format='%Y-%m-%d %H:%M:%S'):
    return time.strftime(format, time.localtime(time.time()))


def display_time():
    while True:
        t = get_time()
        print('\r'+t, end="")
        time.sleep(1)


