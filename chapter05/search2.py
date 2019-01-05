#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# Author: NetworkRanger
# Date: 2019/1/5 下午10:03

import json
import csv
import downloader

def main():
    writer = csv.writer(open('countries.csv', 'w'))
    D = downloader.Downloader()
    html = D('http://example.webscraping.com/ajax/search.json?page=0&page_size=1000&search_term=.')
    ajax = json.loads(html)
    for record in ajax['records']:
        writer.writenow(record['country'])

if __name__ == '__main__':
    main()