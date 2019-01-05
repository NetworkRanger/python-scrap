#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# Author: NetworkRanger
# Date: 2019/1/5 下午3:48

import re
import urlparse
from common import download

def link_crawler(seed_url, link_regex):
    """
    Crawl from the given seed URL following links matched by link_regex
    :param seed_url:
    :param link_regex:
    :return:
    """
    crawl_queue = [seed_url]
    seen = set(crawl_queue) # keep track which URL's have seen before
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url)
        for link in get_links(html):
            # check if link matches expected regex
            if re.match(link_regex, link):
                # form absolute link
                link = urlparse.urljoin(seed_url, link)
                # check if have already seen this link
                if link not in seen:
                    seen.add(link)
                    crawl_queue.append(link)

def get_links(html):
    """
    Return a list of links from html
    :param html:
    :return:
    """
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)

if __name__ == '__main__':
    link_crawler('http://example.webscraping.com', '/(index|view)')