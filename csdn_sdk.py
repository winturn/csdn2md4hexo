#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import conf
import json

class Csdn(object):
    def __init__(self):
        self.app_key = conf.app_key
        self.app_secret = conf.app_secret
        self.user_name = conf.user_name
        self.user_passwd = conf.user_passwd
        self.access_token = None

    def _get(self, *args, **kwargs):
        res = requests.get(*args, **kwargs)
        res_json = json.loads(res.text.replace('\t', '\\t'))
        if 'error_code' in res_json:
            raise Exception('{err_code}: {err_msg}'.format(
                err_code=res_json['error_code'], err_msg=res_json['error']))
        return res_json

    def get_oauth2(self):
        oauth2_url = (
            'http://api.csdn.net/oauth2/access_token'
            '?client_id={app_key}&client_secret={app_secret}&grant_type=password'
            '&username={user_name}&password={user_passwd}'.format(
                app_key=self.app_key, app_secret=self.app_secret,
                user_name=self.user_name, user_passwd=self.user_passwd))
        res = self._get(url=oauth2_url)
        self.access_token = res['access_token']
        return self.access_token

    def user_getinfo(self):
        url = 'http://api.csdn.net/user/getinfo'
        params = {'access_token': self.access_token}
        res = self._get(url=url, params=params)
        return res

    def blog_getinfo(self):
        url = 'http://api.csdn.net/blog/getinfo'
        params = {'access_token': self.access_token}
        res = self._get(url=url, params=params)
        return res

    def blog_getarticlelist(self, status='enabled', page=1, size=15):
        url = 'http://api.csdn.net/blog/getarticlelist'
        params = {
            'access_token': self.access_token,
            'status': status,
            'page': page,
            'size': size}
        res = self._get(url=url, params=params)
        return res

    def blog_getarticle(self, num):
        url = 'http://api.csdn.net/blog/getarticle'
        params = {
            'access_token': self.access_token,
            'id': num}
        res = self._get(url=url, params=params)
        return res




