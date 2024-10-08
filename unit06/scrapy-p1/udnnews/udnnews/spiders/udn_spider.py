import scrapy
import json


class UdnSpiderSpider(scrapy.Spider):
    name = "udn_spider"
    allowed_domains = ["udn.com"]
    
    def __init__(self, *args, **kwargs):
        super(UdnSpiderSpider, self).__init__(*args, **kwargs)
        self.page = 1
        self.api_url = "https://udn.com/api/more?page={}&channelId=1&type=breaknews"

    def start_requests(self):
        yield scrapy.Request(self.api_url.format(self.page), callback=self.parse_api)

    def parse_api(self, response):
        data = json.loads(response.text)
        
        for item in data['lists']:
            yield {
                'title': item['title'],
                'summary': item['paragraph'],
                'url': f"https://udn.com{item['titleLink']}",
                'time': item['time']['date'],
                'view': item['view']
            }

        if not data['end']:
            self.page += 1
            yield scrapy.Request(self.api_url.format(self.page), callback=self.parse_api)
