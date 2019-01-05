#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# Author: NetworkRanger
# Date: 2019/1/5 下午8:46

from datetime import datetime, timedelta
from pymongo import MongoClient, errors

class MongoQueue:
    """
    >>> timeout = 1
    >>> url = 'http://example.webscraping.com'
    >>> q = MongoQueue(timeout=timeout)
    >>> q.clear() # ensure empty queue
    >>> q.push(url) # add test URL
    >>> q.peek() == q.pop() == url # pop back this URL
    True
    >>> q.repair() # immediate repair will do nothin
    >>> q.pop() # another pop should be empty
    >>> import time; time.sleep(timeout) # wait for timeout
    >>> q.repair() # now repair will release URL
    REleased: test
    >>> q.pop() == url # pop URL again
    True
    >>> bool(q) # queue is still active while outstanding
    True
    >> q.complete(url) # complete is URL
    >> bool(q) # queue is not complete
    False
    """

    # possible states of a download
    OUTSTANDING, PROCESSING, COMPILE = range(3)

    def __init__(self, client=None, timeout=300):
        """
        :param host: the host to connect to MongoDB
        :param port: the port to connect to MongoDB
        :param timeout: the numer of seconds to allow for a timeout
        """
        self.client = MongoClient() if client is None else client
        self.db = self.client.cache
        self.timeout = timeout

    def __nozero__(self):
        """
        Returns True if there area more jobs to process
        :return: bool
        """
        record = self.db.crawl_queue.find_one(
            {'status': {'$ne': self.COMPILE}}
        )
        return True if record else False

    def push(self, url):
        """
        Add new URL to queue if does not exist
        :param url:
        :return:
        """
        try:
            self.db.crawl_queue.insert({'_id': url, 'status': self.OUTSTANDING})
        except errors.DuplicateKeyError as e:
            pass # this is already in the queue

    def pop(self):
        """
        Get an outstanding URL from the queue and set its status to processing.
        If the queue is empty a KeyError exception is raised.
        :return:
        """
        record = self.db.crawl_queue.find_and_modify(
            query={'status': self.OUTSTANDING},
            update={'$set', {'status': self.PROCESSING, 'timestamp': datetime.now()}}
        )
        if record:
            return record['_id']
        else:
            self.repair()
            raise KeyError

    def peek(self):
        record = self.db.crawl_queue.find_one({'status': self.OUTSTANDING})
        if record:
            return record['_id']

    def complete(self, url):
        self.db.crawl_queue.update({'_id': url}, {'$set': {'status': self.COMPILE}})

    def repair(self):
        """
        Release stalled jobs
        :return:
        """
        record = self.db.crawl_queue.find_and_modify(
            query={
                'timestamp': {'$lt', datetime.now() - timedelta(seconds=self.timeout)},
                'status': {'$ne', self.COMPILE}
            },
            update={'$set': {'status': self.OUTSTANDING}}
        )
        if record:
            print 'Releases:', record['_id']

    def clear(self):
        self.db.crawl_queue.drop()