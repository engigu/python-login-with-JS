#!/usr/bin/env python
# coding:utf-8

import requests
from hashlib import md5


class RClient(object):
    def __init__(self, username, password, soft_id, soft_key):
        self.username = username
        m = md5()
        m.update(password)
        self.password = m.hexdigest()
        self.soft_id = soft_id
        self.soft_key = soft_key
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    def rk_create(self, im, im_type, timeout=60):
        """
        im: 图片字节
        im_type: 题目类型
        """
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('a.jpg', im)}
        r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers)
        return r.json()

    def rk_report_error(self, im_id):
        """
        im_id:报错题目的ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
        return r.json()


def get_result(type,img_obj):
    # 	66373	0347bd9564cd499f83c0a29412a68b61
    username = 'a451292130'
    password = 'Gq19940507'
    soft_id = '66373'
    soft_key = '0347bd9564cd499f83c0a29412a68b61'
    rc = RClient(username, password.encode(), soft_id, soft_key)
    # im = open('a.jpg', 'rb').read()
    # with open(path, 'rb') as f:
    #     im = f.read()
    return rc.rk_create(img_obj, type)


if __name__ == '__main__':
    print(get_result('a.jpg',3040))
