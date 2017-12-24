import traceback

import requests
import json
import os, sys

import time

base_dir = os.path.dirname(os.path.abspath(__file__))
# json_dir = os.path.join(base_dir, 'json')
json_dir = "."
sys.path.append(base_dir)
import settings


def get_time(format='%Y-%m-%d %H:%M:%S'):
    return time.strftime(format, time.localtime(time.time()))


class ProductCodes(object):
    def __init__(self, url=settings.BET_CODE_URL, file_path=os.path.join(json_dir, settings.PROPERTY_CODE_FILE)):
        self._url = url
        self._file_path = file_path
        self._rs_path = get_time('%Y%m%d')

    def get_rs_path(self):
        path = get_time('%Y%m%d')
        if not os.path.exists(path):
            os.mkdir(path)
            self._rs_path = path
        return self._rs_path

    def write_json_to_file(self, data):
        """把data设置到环境变量

        :param data:
        :return:
        """
        # os.environ.setdefault(settings.TOUZHU_JSON_DATA, json.dumps(data))
        with open(self._file_path, 'w') as f:
            f.write(str(data))

    def save_response(self, property, rs):
        try:
            file_path = "./" +self.get_rs_path() + '/' + str(property) + '.json'
            with open(file_path, 'w')as f:
                f.write(json.dumps(rs))
        except Exception as e:
            traceback.print_exc()
            pass

    def get_json(self, property):

        def get_period():
            try:
                url = self._url + str(property)
                rs = requests.get(url, timeout=10)

                if rs.status_code == 200:
                    return rs.json()
                else:
                    print('get xiazhu json satatus code: '+str(rs.status_code))
                    return None
            except Exception as e:
                traceback.print_exc()
                print("Get xhiazhu json except")
                return None

        js = get_period()
        if js is None:
            time.sleep(3)
            return get_period()
        else:
            return js


    def save_current_json(self, property):
        '''

        :param property:
        :return:  False: 不投注
        '''
        data = self.get_json(property)
        if data is None:  # 获取号码失败
            return False
        else:   # 正常获取
            self.write_json_to_file(json.dumps(data))
            self.save_response(property, data)
            return True

if __name__ == "__main__":
    pr = ProductCodes()
    for i in ['20171208001','20171208002','20171208003','20171208004']:
        print(pr.save_current_json(i)[1])
        time.sleep(1)

