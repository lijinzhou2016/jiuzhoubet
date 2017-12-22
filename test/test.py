import requests
import time

def post_data():
    data = {
        "gid": 20171206093,
        "gType": 24,
        "kType": 197,
        "lType": 197,
        "spType": "oneStar",
        "count": 1,
        "delGid": "",
        "bType": "53;;;;",
        "wOdds": "1.99;;;;",
        "amt": 200,
        "betTime": "GMT+8 2017-12-6 21:26:10"
    }

    url = 'https://ts111c.storei.net/game/ajax/wagers/AddAnyTime.aspx'
    headers = {"Cookie": "ASP.NET_SessionId=j2wujq2c2g14hfrcq3grufxc"}
    post_data = {'betData': str(data)}

    rs = requests.post(url, data=post_data, headers=headers, timeout=5)
    print(rs.status_code)
    print(rs.text)


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


# display_time()

while 2>3:
    pass
else:
    print("hhhhh")
