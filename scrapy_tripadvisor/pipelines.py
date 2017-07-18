# -*- coding: utf-8 -*-

import re
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request


class DownloadImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for each in item['image_urls']:
            yield Request(each, meta={'item': item})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        # 图片文件名
        image_guid = re.findall('com/(.*).jpg', item['image_urls'][0])[0].replace('/', '-')
        filename = 'full/{0}/{1}.jpg'.format(item['location'], image_guid)
        return filename
