import scrapy


class LianjiaZfItem(scrapy.Item):
    title = scrapy.Field()  # 标题
    update_time = scrapy.Field()  # 房源更新时间
    price = scrapy.Field()  # 月租
    tags = scrapy.Field()  # 标签
    rent_method = scrapy.Field()  # 出租方式
    house_type = scrapy.Field()  # 房屋类型
    towards_and_floor = scrapy.Field()  # 朝向楼层
    basic_info = scrapy.Field()  # 房屋信息
    supporting_facilities = scrapy.Field()  # 配套设施
    description = scrapy.Field()  # 房源描述
    url = scrapy.Field()  # 详情页链接

