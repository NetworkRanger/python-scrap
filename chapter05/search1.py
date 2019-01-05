#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# Author: NetworkRanger
# Date: 2019/1/5 下午9:59

import json
import string
import downloader
import mongo_cache

FIELDS = ('area', 'population', 'iso', 'country', 'capital', 'continent', 'tld', 'currency_code', 'currency_name', 'phone', 'postal_code_format', 'postal_code_regex', 'languages', 'neighbours')

def main():
    template_url = 'http://example.webscraping.com/ajax/search.json?page={}&page_size=10&search_item={}'
    countries = set()
    download = downloader.Downloader(mongo_cache.MongoCache())

    for letter in string.lowercase:
        page = 0
        while True:
            html = download(template_url.format(page, letter))
            try:
                ajax = json.loads(html)
            except ValueError as e:
                print e
                ajax = None
            else:
                for record in ajax['records']:
                    countries.add(record['contry'])
            page += 1
            if ajax is None or page >= ajax['num_pages']:
                break

    open('countries.txt', 'w').write('\n'.join(sorted(countries)))

if __name__ == '__main__':
    main()