# -*- coding: utf-8 -*-
import base64
import json
from gluon import cache

from gluon.tools import fetch


class Iugu(object):
    url = "https://api.iugu.com/v1/"

    def __init__(self, token):
        self.token = token
        base64string = base64.encodestring('%s:%s' % (token, "")).replace('\n', '')
        self.headers = {'Authorization': "Basic %s" % base64string}

    def _fetch(self, url, data=None):
        return json.loads(fetch(url, data, self.headers))

    def _simple_get(self, item):
        url = self.url + item
        r = self._fetch(url)
        return r
