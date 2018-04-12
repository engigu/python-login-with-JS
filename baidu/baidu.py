import execjs
import requests


class BaiDu(object):


    def __init__(self):
        self.get_pwd_url = 'https://raw.githubusercontent.com/EngiGu/python-login-with-JS/master/baidu/pwd.js'

    def _encrypt_pwd(self,pwd):
        js_content = requests.get(self.get_pwd_url).content.decode()

        js_engine = execjs.get()
        cm = js_engine.compile(js_content)
        return cm.call('enbdpwd', pwd)


if __name__ == '__main__':
    b = BaiDu()
    print(b._encrypt_pwd('admin123'))