import requests

from sendermsg import Phone


url = "http://47.104.31.179/project/CheckPhone?phone={0}"

class Users(object):
    def __init__(self):
        self.phone = Phone()
        self._ph = ""

    def input_user(self):
        for i in range(3):
            user = input("请输入账号:")
            if self.phone.is_phone(user):
                return user
            else:
                print("！！！账号格式不对！！！")
        return None

    def check_user(self):
        user = self.input_user()
        if user:
            try:
                rs = requests.get(url.format(user), timeout=10)
                if rs.status_code == 200:
                    self._ph = user
                    self.save_phone(user)
                    return rs.json()["result"]
            except Exception as e:
                print(str(e))
                return False
    def get_phone(self):
        return self._ph

    def save_phone(self, user):
        with open(".user", 'w') as f:
            f.write(user)


if __name__ == "__main__":
    u = Users()
    print(u.check_user())

