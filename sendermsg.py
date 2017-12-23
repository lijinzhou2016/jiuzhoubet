# coding:utf-8

import requests
import re

YD = ['134', '135', '136', '137', '138', '139', '150', '151', '157', '158', '159', '187', '188']  # 移动
DX = ['133', '153', '180', '189']  # 电信
LT = ['130', '131', '132', '152', '155', '156', '185', '186']  # 联通

class Phone(object):
    def __init__(self, phone=""):
        self._phone = phone

    def get_phone(self):
        return self._phone

    def set_phone(self, phone):
        self._phone = phone

    def is_phone(self, phone=None):
        """
        验证手机号是否合法
        :param phone:
        :return:
        """
        if not phone:
            phone = self.get_phone()
        reg = r'^((13[0-9])|(15[^4,\D])|(18[0,0-9]))\d{8}$'
        if re.match(reg, phone):
            return True
        else:
            return False

    def get_operatiot(self, phone=None):
        """
        获取手机号的运营商
        :param phone:
        :return:
        """
        if not phone:
            phone = self.get_phone()
        for top in DX:
            if phone.startswith(top):
                return "DX"
        for top in YD:
            if phone.startswith(top):
                return "YD"

        return "UNKNOWN"


class Sender(object):
    def __init__(self, phone, operatior):
        self._sphones = phone
        self._operatior = operatior
        self._api = "YidaInterface/SendSms.do?sname={0}&spwd={1}&sphones={2}&smsg={3}&msg_id={4}&scorpid={5}"
        self._sname = "zw2017"
        self._spwd = "111111"
        self._msg_id = ""
        self._scorpid = ""

    def send(self, msg):
        url = self.format_url(msg)
        try:
            rs = requests.get(url, timeout=10)
            print(rs.text)
        except Exception as e:
            print(str(e))

    def format_url(self, msg):
        server = self.get_server(self._operatior)
        return "/".join([server,
                         self._api.format(self._sname, self._spwd, self._sphones, msg, self._msg_id, self._scorpid)])

    def get_server(self, operatior):
        m = {
            "YD": "http://223.68.139.178:9010",
            "DX": "http://221.226.28.36:9010",
            "LT": ""
        }
        return m.get(operatior)

if __name__ =="__main__":
    p="13770976640"
    phone = Phone(p)
    if phone.is_phone():
        print(phone.get_operatiot())
        sender = Sender(p, phone.get_operatiot())
        sender.send("哈哈哈")


