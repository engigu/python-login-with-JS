import re
from time import time

import execjs
import requests

import config
from rkdama import rk

class BaiduWap(object):

    def __init__(self,user,pwd):
        self.user = user
        self.pwd = pwd
        self.start_url = 'http://wappass.baidu.com/passport/?login&tpl=wimn&subpro=wimn&regtype=1&u=https%3A%2F%2Fm.baidu.com/usrprofile%23logined'
        self.tt = str(round(time() * 1000))
        self.serverTime = None
        self.login_url = 'https://wappass.baidu.com/wp/api/login?tt=%s' % self.tt
        self.session = requests.session()
        self.headers = {
            'Host': 'wappass.baidu.com',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'https://m.baidu.com/usrprofile?action=home&model=user&ori=index',
        }

    # check verify code
    def _check_code(self,gid,user,traceid):

        check_url = 'https://wappass.baidu.com/wp/api/login/check?gid=%s&tt=%s&username=%s' \
                    '&countrycode=&clientfrom=wap&sub_source=leadsetpwd&tpl=wimn&traceid=' \
                    '%s' % (gid,self.tt,user,traceid)
        print(check_url)

        tmp = self.session.get(check_url)
        print(tmp.json())
        codeString = tmp.json()['data'].get('codeString')
        # need verify code
        if codeString:
            code_url = 'https://wappass.baidu.com/cgi-bin/genimage?%s&v=%s' % (codeString,self.tt)
            content = self.session.get(code_url)
            print('*'*10)
            code = rk.get_result(3040,content.content)
            print(code)
            print(gid,user,traceid)
            # TODO 目前百度验证码校验不成功，有待解决
            return {'stats':1,'code':code['Result'],'codeString':codeString}
        return {'stats':0,'code':None}


    def _get_params(self,gid):
        self.session.get('http://wap.baidu.com')
        self.session.get('http://wappass.baidu.com/passport/')
        tmp = self.session.get(self.start_url, headers=self.headers)
        # print(self.session.cookies)

        tmp_comtent = tmp.content.decode()
        # print(tmp_comtent)
        tmp_re = re.findall(r'(https%3A%2F%2Fm.baidu.com%2Fusrprofile%3Fuid%3D(\w+)%26traceid%3D(\w+)%23logined)',
                            tmp_comtent)
        print(tmp_re)
        getpassurl = re.findall(r'id="getpassUrl" name="getpassUrl" value="(.*?)">',tmp_comtent)
        # fp_uid_tmp = re.findall(r'fp_uid="(.*?)"',tmp_comtent)

        serverTime_url = 'http://wappass.baidu.com/wp/api/security/antireplaytoken?tpl=wimn&v=%s&traceid=%s' % (
            self.tt,tmp_re[0][2])
        tmp_serverTime = self.session.get(serverTime_url).json()
        print(tmp_serverTime)
        self.serverTime = tmp_serverTime.get('time')

        post_data = {
            'username': self.user,
            'password': '',
            'verifycode': '',
            'vcodestr': '',
            'action': 'login',
            'u': tmp_re[0][0],
            'tpl': 'wimn',
            'tn': '',
            'pu': '',
            'ssid': '',
            'from': '',
            'bd_page_type': '',
            'uid': tmp_re[0][1],
            'type': '',
            'regtype': '',
            'subpro': 'wimn',
            'adapter': '0',
            'skin': 'default_v2',
            'regist_mode': '',
            'login_share_strategy': '',
            'client': '',
            'clientfrom': '',
            'connect': '0',
            'bindToSmsLogin': '',
            'isphone': '0',
            'loginmerge': '1',
            'getpassUrl': getpassurl[0],
            'dv': 'tk0.1217801861598281523531590750@tts0QvrD9CsmlCFb7YFV--9bHWFaogJG~jrkqirK~xrm~~84lRJbLU8KHjJK2UMp-L8ksis3BxSkn~sV~~84lRJbLU8KHjJK2UMp-L8ksisjBlSkn~sG~~84lRJbLU8KHjJK2UMp-L8ksiAk9lSkn~sW~~84lRJbLU8KHjJK2UMp-L8ksiA3EzSq__xnnNynE4fjjNhEsIsG~lsG~lsB__~sM74C~83nWsD9iskniA3n-rD0Wrkn-s3s-sjn-rDqzADq_gsL8tHUJ4HaNpxLJq__CsMsm~~8knWAksCs3u~rm~ZsDBCAjsb8kBlAm~ZsDBCAjsb',
            'countrycode': '',
            'mobilenum': 'undefined',
            'servertime': self.serverTime,
            'gid': '',
            'logLoginType': 'wap_loginTouch',
            'FP_UID': '',  # TODO 暂时未解决这个参数，这个参数来自于网页设置的cooikes
            'traceid': tmp_re[0][2],

        }


        ret = self._check_code(gid,user=self.user,traceid=tmp_re[0][2])
        if ret['stats']:
            post_data['verifycode'] = ret['code']
            post_data['vcodestr'] = ret['codeString']
            print(ret['code'],ret['codeString'])
            return post_data
        return post_data


    def encrypt_pwd(self):
        # serverTime = 'e1a6f1d17c'
        with open('./pwd_wap.js', 'r', encoding='utf-8') as f:
            js_content = f.read()

        # encrypt
        js_engine = execjs.get()
        cm = js_engine.compile(js_content)
        gid = cm.call('guideRandom')
        post_data = self._get_params(gid)

        # replace JS params
        # print(self.serverTime)
        js_content = js_content.replace('{{serverTime}}', 'var serverTime="%s";' % self.serverTime)
        js_content = js_content.replace('{{module}}', 'var module="%s";' % config.MODULE)

        cm = js_engine.compile(js_content)
        en_pwd  = cm.call('enbaidupwd', self.pwd)

        post_data['password'] = en_pwd

        post_data['gid'] = gid
        print(post_data)
        return post_data

    def login(self):
        post_data = self.encrypt_pwd()
        content = self.session.post(self.login_url,data=post_data,headers=self.headers)
        print(content.content.decode())



if __name__ == '__main__':
    b = BaiduWap('13148304735','gq19940507')
    # b._get_params()
    # print(b.encrypt_pwd('admin1234'))
    b.login()