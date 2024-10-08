import scrapy
import json
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class NewsSpiderSpider(scrapy.Spider):
    name = "news_spider"
    allowed_domains = ["udn.com"]
    start_urls = ["https://udn.com/news/breaknews/1"]
    
    def __init__(self, *args, **kwargs):
        super(NewsSpiderSpider, self).__init__(*args, **kwargs)
        self.page = 1
        self.max_pages = 10  # 設定最大頁數為10
        
        # 連接MongoDB
        self.client = MongoClient("mongodb://admin:mymdb$1234@localhost:27017")
        self.db = self.client["unit06db"]
        self.collection = self.db["udnnews"]
        
        # 創建索引以確保URL的唯一性
        self.collection.create_index("url", unique=True)

    def parse(self, response):
        # 解析初始頁面的新聞項目
        news_items = response.css('div.story-list__news')
        for item in news_items:
            news_item = {
                'title': item.css('h2::text').get(),
                'url': response.urljoin(item.css('a::attr(href)').get()),
                'date_time': item.css('time::text').get()
            }
            self.save_to_mongo(news_item)
        
        # 發送API請求以獲取更多新聞
        if self.page < self.max_pages:
            api_url = f"https://udn.com/api/more?page={self.page}&id=&channelId=1&cate_id=0&type=breaknews&totalRecNo=10050"
            yield scrapy.Request(api_url, callback=self.parse_api)

    def parse_api(self, response):
        data = json.loads(response.text)
        if data['lists']:
            for item in data['lists']:
                if item['title'].strip() is None or len(item['title'].strip()) < 5 or item['title'].strip() == '':
                    continue
                news_item = {
                    'title': item['title'],
                    'url': 'https://udn.com' + item['titleLink'],
                    'date_time': item['time']['date']
                }
                self.save_to_mongo(news_item)
            
            # 如果還沒達到最大頁數,繼續請求
            self.page += 1
            if self.page < self.max_pages:
                next_url = f"https://udn.com/api/more?page={self.page}&id=&channelId=1&cate_id=0&type=breaknews&totalRecNo=10050"
                yield scrapy.Request(next_url, callback=self.parse_api)

    def save_to_mongo(self, item):
        try:
            self.collection.insert_one(item)
        except DuplicateKeyError:
            self.logger.info(f"Duplicate item found: {item['url']}")

    def closed(self, reason):
        self.client.close()
