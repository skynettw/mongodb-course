import scrapy
import json
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

class NewsSpiderSpider(scrapy.Spider):
    name = "news_spider"
    allowed_domains = ["udn.com"]
    start_urls = ["https://udn.com/news/breaknews/1"]
    api_url = "https://udn.com/api/more"
    page = 1
    max_pages = 5

    def __init__(self, *args, **kwargs):
        super(NewsSpiderSpider, self).__init__(*args, **kwargs)
        # 連接到 MongoDB
        self.client = MongoClient("mongodb://admin:mymdb$1234@localhost:27017")
        self.db = self.client["unit05db"]
        self.collection = self.db["udnnews"]
        # 創建唯一索引以避免重複
        self.collection.create_index([("url", 1)], unique=True)

    def parse(self, response):
        # 處理初始頁面
        yield from self.parse_news_list(response)
        
        # 繼續請求下一頁
        yield scrapy.FormRequest(
            url=self.api_url,
            method='GET',
            formdata={
                'page': str(self.page + 1),
                'id': '',
                'channelId': '1',
                'cate_id': '0',
                'type': 'breaknews',
                'totalRecNo': '10050'
            },
            callback=self.parse_api_response
        )

    def parse_api_response(self, response):
        data = json.loads(response.text)
        
        # 解析 API 返回的新聞列表
        for item in data.get('lists', []):
            news_url = f"https://udn.com{item.get('titleLink')}"
            yield scrapy.Request(news_url, callback=self.parse_news_content, meta={
                'title': item.get('title'),
                'date': item.get('time'),
            })
        
        # 檢查是否需要繼續爬取下一頁
        self.page += 1
        if self.page < self.max_pages:
            yield scrapy.FormRequest(
                url=self.api_url,
                method='GET',
                formdata={
                    'page': str(self.page + 1),
                    'id': '',
                    'channelId': '1',
                    'cate_id': '0',
                    'type': 'breaknews',
                    'totalRecNo': '10050'
                },
                callback=self.parse_api_response
            )

    def parse_news_list(self, response):
        news_list = response.css('div.story-list__news')
        if not news_list:
            self.logger.warning(f"在 {response.url} 沒有找到新聞列表")
            return

        for news in news_list:
            news_url = news.css('a::attr(href)').get()
            if news_url:
                yield scrapy.Request(response.urljoin(news_url), callback=self.parse_news_content, meta={
                    'title': news.css('h2::text').get(),
                })

        next_page = response.css('a.pagination__next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_news_content(self, response):
        content = ' '.join(response.css('div.article-content__paragraph p::text').getall()).strip()
        news_item = {
            'title': response.meta.get('title'),
            'url': response.url,
            'date': response.meta.get('date'),
            'content': content
        }
        self.save_to_mongodb(news_item)

    def save_to_mongodb(self, item):
        try:
            self.collection.insert_one(item)
        except DuplicateKeyError:
            self.logger.info(f"重複的新聞項目: {item['url']}")

    def closed(self, reason):
        self.client.close()
