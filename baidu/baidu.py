import json

import execjs
import requests

import config


class BaiDu(object):
    '''use online JS url to get config,
        For Baidu encrypt JS, the pubkey is fixed,
        U can change pubkey with PWD_PUBKEY_URL in config file.
    '''

    def __init__(self):
        self.get_pwd_url = 'https://raw.githubusercontent.com/EngiGu/python-login-with-JS/master/baidu/pwd.js'

    def _encrypt_pwd(self,pwd):
        pub_key_content = requests.get(config.PWD_PUBKEY_URL).content.decode()
        pub_key_content = json.loads(pub_key_content.replace("'",'"'))
        pub_key = pub_key_content.get('pubkey')
        if pub_key:
            js_content = requests.get(self.get_pwd_url).content.decode()
            temp = 'var pubkey = "%s";' % pub_key
            js_content = js_content.replace('{{pubkey}}',temp)

            # encrypt
            js_engine = execjs.get()
            cm = js_engine.compile(js_content)
            return cm.call('enbdpwd', pwd)


if __name__ == '__main__':
    b = BaiDu()
    print(b._encrypt_pwd('admin123'))