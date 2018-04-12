import json

import execjs
import requests
import config

# pwd_JS_url = 'https://raw.githubusercontent.com/EngiGu/python-login-with-JS/master/baidu/pwd.js'

# js_content = requests.get(pwd_JS_url).content.decode()
# print(js_content)
with open('./pwd.js','r',encoding='utf-8') as f:
    js_content = f.read()

# get pubkey
pubkey_content = requests.get(config.PWD_PUBKEY_URL).content.decode()
pubkey_content = json.loads(pubkey_content.replace("'",'"'))
# print(pubkey_content)
pubkey = pubkey_content.get('pubkey')
print(pubkey)

# encrypt pwd
js_engine = execjs.get()
cm = js_engine.compile(js_content)
print(cm.call(pubkey,'enbdpwd'))
