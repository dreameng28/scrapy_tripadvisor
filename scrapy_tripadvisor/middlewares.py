# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
from scrapy import signals


class RandomAgent(object):
    """ it is used to change angent
    """

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_resquest(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.agents))


class ProxyMiddler(object):
    """ it is used to set proxy
    """

    def __init__(self, proxys):
        self.proxys = proxys

    @classmethod
    def from_crawler(cls, crawler):
        proxys = crawler.settings.getlist('PROXIES')
        return cls(proxys)

    def process_request(self, request, spider):
        proxy = random.choice(self.proxys)

        if proxy['ip_port']:
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
