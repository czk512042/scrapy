# -*- coding: utf-8 -*-
import scrapy
from items import LianjiaZfItem


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://sz.lianjia.com/zufang/']

    def parse(self, response):
        house_items = response.xpath('//*[@id="content"]/div[1]/div[1]/child::div')
        for house_item in house_items:
            href_xpath = './a/@href'
            house_url = house_item.xpath(href_xpath).get()
            if "zufang" in house_url:
                yield scrapy.Request(response.urljoin(house_url), callback=self.parse_details)

        next_page = response.xpath('//*[@id="content"]/div[1]/div[2]/a[6]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_details(self, response):
        item = LianjiaZfItem()

        item['url'] = response.url

        title_xpath = '//p[@class="content__title"]/text()'
        item['title'] = response.xpath(title_xpath).get().strip()

        update_time_xpath = '//div[@class="content__subtitle"]/text()'
        item['update_time'] = response.xpath(update_time_xpath).get().split('：')[-1].strip()

        price_xpath = '//div[@class="content__aside--title"]/span//text()'
        unit_xpath = '//div[@class="content__aside--title"]/text()'
        item['price'] = response.xpath(price_xpath).get().strip() + \
                        response.xpath(unit_xpath).getall()[1].split(' ')[0].strip()

        tags_xpath = '//p[@class="content__aside--tags"]//text()'
        item['tags'] = [item.strip() for item in response.xpath(tags_xpath).getall() if item.strip()]

        rent_xpath = '//*[@id="aside"]/ul[1]//li/text()'
        rent_data = response.xpath(rent_xpath).getall()
        item['rent_method'] = rent_data[0].strip()
        item['house_type'] = rent_data[1].strip()
        item['towards_and_floor'] = rent_data[2].strip()

        basic_info_xpath = '//*[@id="info"]//li/text()'
        basic_infos = response.xpath(basic_info_xpath).getall()
        basic_info = {}
        for bi in basic_infos:
            if '：' in bi:
                basic_info[bi.split('：')[0].strip()] = bi.split('：')[1].strip()
        item['basic_info'] = basic_info

        supporting_facilities_xpath = '//ul[@class="content__article__info2"]/li[@class="fl oneline  "]/text()'
        supporting_facilities = [item.strip() for item in response.xpath(supporting_facilities_xpath).getall() if item.strip()]
        item['supporting_facilities'] = supporting_facilities

        description_xpath = '//p[@data-el="houseComment"]/@data-desc'
        description = response.xpath(description_xpath).get()
        item['description'] = description.strip() if description else ''

        return item
