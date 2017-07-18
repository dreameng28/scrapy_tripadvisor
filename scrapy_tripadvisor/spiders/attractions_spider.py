# -*-coding:utf-8 -*-

import re
import scrapy
import logging
from bs4 import BeautifulSoup
from scrapy.http import Request
from scrapy_tripadvisor.items import AttractionItem

# the pictures url
CALL_PICTURE_URL = 'https://www.tripadvisor.cn/LocationPhotoAlbum?geo={geo}&detail={detail}&albumViewMode=heroThumbs&albumid=101&thumbnailMinWidth=50&cnt=30&offset={offset}&filter=7&heroMinWidth=1863&heroMinHeight=939&albumPartialsToUpdate=partial'

logger = logging.getLogger('mycustomlogger')


class AtrractionSpider(scrapy.Spider):
    """it is used to collect the attraction information from
       the website
    """
    name = 'attractionspider'

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.start_urls = ['https://www.tripadvisor.cn/Attractions-g294212-Activities-Beijing.html']
        self.head = 'https://www.tripadvisor.cn'
        self.rules = ()

    def start_requests(self):
        for url in self.start_urls:
            request = Request(url)

            yield request

    def parse(self, response):
        html = BeautifulSoup(response.body)

        page_html = html.find('div', class_='pageNumbers').find_all('a')
        page_number = page_html[-1].text

        for page in range(int(page_number)):
            if page == 0:
                page_pic_url = response.url
            else:
                page_str = 'oa' + str(page * 30)
                url_list = response.url.split('-')
                url_list.insert(-1, page_str)
                page_pic_url = '-'.join(url_list)

            yield Request(page_pic_url, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        html = BeautifulSoup(response.body)
        geo = response.url.split('-')[1]
        div_attr = html.find_all('div', id='ATTR_ENTRY_')

        for div_item in div_attr:
            item = AttractionItem()
            item['geo'] = geo
            image_info = div_item.find(class_=re.compile('photo_booking')).a
            item['location'] = div_item['data-locationid']
            item['url'] = image_info['href']
            request = Request(self.head + item['url'], callback=self.parse_item)
            request.meta['item'] = item

            yield request

    def parse_item(self, response):
        item = response.meta['item']
        url = response.url
        html_soup = BeautifulSoup(response.body)
        try:
            title = html_soup.find('h1', id='HEADING').text
            head_html = html_soup.find('div', class_='rating_and_popularity')
            score = head_html.find('span', class_='header_rating').find('span')['content']
            des_html = head_html.find('span', class_='header_detail attraction_details').find_all('a')
            count_text = html_soup.find('div', class_='see_all_count_wrap').find('span', class_='see_all_count').text
            count = ''.join(re.findall(r'(\d+)', count_text))
            geo = item['geo']
            _id = re.findall(r'(\d+)', url.split('-')[2])[0]
            num = int(count) / 30 + 1

            item['title'] = title
            item['score'] = score
            item['count'] = count
            item['tag'] = [des.text for des in des_html]

            for time in range(num + 1):
                offset = 30 * time
                detail_url = self.get_call_picture_url(geo, _id, offset, int(count))

                if detail_url:
                    request = Request(detail_url, callback=self.parse_detail)
                    request.meta['item'] = item
                    yield request
        except Exception as e:
            pass

    def parse_detail(self, response):
        filename = re.findall(r'offset=(.*)&filter', response.url)[0]
        item = response.meta['item']
        html_soup = BeautifulSoup(response.body)

        pictures = html_soup.find_all('div', id=re.compile('thumb-'), class_='tinyThumb smallLoading ')

        for pic in pictures:
            item['image_urls'] = [pic.get('data-bigurl', '')]
            item['pic_des'] = pic.get('data-captiontext', '')
            item['pic_captionprovider'] = pic.get('data-captionprovider', '')

            yield item

    def get_call_picture_url(self, geo, detail, offset, count):
        if offset < count:
            return CALL_PICTURE_URL.format(geo=geo, detail=detail, offset=offset)
        else:
            return None
