import pymongo


class LianjiaZfPipeline(object):
    def __init__(self, MONGO_HOST, MONGO_PORT, MONGO_DB, MONGO_COL):
        self.MONGO_HOST = MONGO_HOST
        self.MONGO_PORT = MONGO_PORT
        self.MONGO_DB = MONGO_DB
        self.MONGO_COL = MONGO_COL

    @classmethod
    def from_crawler(cls, crawler):
        return cls(MONGO_HOST=crawler.settings.get('MONGO_HOST'),
                   MONGO_PORT=crawler.settings.get('MONGO_PORT'),
                   MONGO_DB=crawler.settings.get('MONGO_DB'),
                   MONGO_COL=crawler.settings.get('MONGO_COL'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host=self.MONGO_HOST, port=self.MONGO_PORT)
        self.col = self.client[self.MONGO_DB][self.MONGO_COL]

    def process_item(self, item, spider):
        find = {'url': item['url']}
        self.col.update(find, {'$set': item}, upsert=True)
        return item

    def close_spider(self, spider):
        self.client.close()
