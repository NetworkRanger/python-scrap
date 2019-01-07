#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# Author: NetworkRanger
# Date: 2019/1/7 下午10:12

import sys
import json
import pprint
from downloader import Downloader


def graph(page_id):
    D = Downloader()
    html = D('http://graph.facebook.com/' + page_id)
    return json.loads(html)


if __name__ == '__main__':
   try:
       page_id = sys.argv[1]
   except IndexError:
       page_id = 'PacktPub'
   pprint.pprint(graph(page_id))