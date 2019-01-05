#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# Author: NetworkRanger
# Date: 2019/1/5 下午3:39

import itertools
from common import download

def iteration():
    max_errors = 5 # maximum number of consecutive download errors allowed
    num_errors = 0 # maximum numer of consecutive download errors
    for page in itertools.count(1):
        url = 'http://example.webscraping.com/view-{}'.format(page)
        html = download(url)
        if html is None:
            # received and error trying to download this webpage
            num_errors += 1
            if num_errors == max_errors:
                # reached maximum amount of erros in a row so exit
                break
            # so assume have reached the last country ID and can stop downloading
        else:
            # success - can scrape the result
            # ...
            num_errors = 0

if __name__ == '__main__':
    iteration()