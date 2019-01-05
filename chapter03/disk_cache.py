#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# Author: NetworkRanger
# Date: 2019/1/5 下午5:43

import os
import re
import urlparse
import shutil
import zlib
from datetime import datetime, timedelta
try:
    import cPickle as pickle
except ImportError:
    import pickle
from link_crawler import link_crawler

class DiskCache:
    """
    Dictionary interface that stores cached
    values in the file system rather than in memory.
    The file path is formed from an md5 hash of the key.

    >>> cache = DiskCache()
    >>> url = 'http://example.webscraping.com'
    >>> result = {'html': '...'}
    >>> cache[url] = result
    >>> cache[url]['html'] = result['html']
    True
    >>> cache = DiskCache(expires=timedelta())
    >>> cache[url] = result
    >>> cache[url]
    Traceback (most recent call last):
    ...
    KeyError: 'http://example.webscraping.com has expired'
    >>> cache.clear()
    """

    def __init__(self, cache_dir='cache', expires=timedelta(days=50), compress=True):
        """
        :param cache_dir: the root level folder for the cache
        :param expire: timedelta of amount of time before a cache entry is considered expired
        :param compress: whether to compress data in the cache
        """
        self.cache_dir = cache_dir
        self.expires = expires
        self.compress = compress

    def __getitem__(self, url):
        """
        Load data from disk for this URL
        :param url:
        :return:
        """
        path = self.url_to_path(url)
        if os.path.exists(path):
            with open(path, 'rb') as fp:
                data = fp.read()
                if self.compress:
                    data = zlib.decompress(data)
                result, timestamp = pickle.loads(data)
                if self.has_expired(timestamp):
                    raise KeyError(url + 'has expired')
                return result
        else:
            # URL has not yet been cached
            raise KeyError(url + ' does not exist')

    def __setitem__(self, url, result):
        """
        Save data to disk for this url
        :param url:
        :param result:
        :return:
        """
        path = self.url_to_path(url)
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)

        data = pickle.dump((result, datetime.utcnow()))
        if self.compress:
            data = zlib.compress(data)
        with open(path, 'wb') as fp:
            fp.write(data)

    def __setitem__(self, url, result):
        """
        Save data to disk for this url
        :param url:
        :param result:
        :return:
        """
        path = self.url_to_path(url)
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)

        data = pickle.dumps((result, datetime.utcnow()))
        if self.compress:
            data = zlib.compress(data)
        with open(path, 'wb') as fp:
            fp.write(data)

    def __delitem__(self, url):
        """
        Remove the value at this key and any empty parent sub-directoies
        :param url:
        :return:
        """
        path = self._key_path(url)
        try:
            os.remove(path)
            os.removdirs(os.path.dirname(path))
        except OSError:
            pass

    def url_to_path(self, url):
        """
        Create file system path for this URL
        :param url:
        :return:
        """
        components = urlparse.urlsplit(url)
        # when empty paht set to /index.html
        path = components.path
        if not path:
            path = '/index.html'
        elif path.endswith('/'):
            path += 'index.html'
        filename = components.netloc + path + components.query
        # replace invalid characters
        filename = re.sub('[^/0-9a-zA-z\-.,;_ ]', '_', filename)
        # restrict maximum number of characters
        filename = '/'.join(segemnt[:255] for segemnt in filename.split('/'))
        return os.path.join(self.cache_dir, filename)

    def has_expired(self, timestamp):
        """
        Return whether this timestamp has expired
        :param timestamp:
        :return:
        """
        return datetime.utcnow() > timestamp + self.expires

    def clear(self):
        """
        Remove all the cached values
        :return:
        """
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)


if __name__ == '__main__':
    link_crawler('http://example.webscraping.com/', '/(index|view)', cache=DiskCache())
