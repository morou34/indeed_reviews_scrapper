import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class AntiBlockerSpider(CrawlSpider):
    name = "antiblocker_spider"
    allowed_domains = ["indeed.com"]
    start_urls = ["http://indeed.com"]
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "myproject.middlewares.RotateUserAgentMiddleware": 543,
            "myproject.middlewares.ProxyMiddleware": 544,
        },
        "DOWNLOAD_DELAY": 2,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_START_DELAY": 1,
        "AUTOTHROTTLE_MAX_DELAY": 3,
    }

    rules = (Rule(LinkExtractor(allow=()), callback="parse_item", follow=True),)

    def parse_item(self, response):
        self.logger.info("Processing page: %s", response.url)
        item = {}
        item["title"] = response.css("title::text").get()
        item["url"] = response.url
        return item


import random
from scrapy import signals


class RotateUserAgentMiddleware:
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
    ]

    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agents)
        request.headers["User-Agent"] = user_agent


class ProxyMiddleware:
    proxies = [
        "http://proxy1.indeed.com:8000",
        "http://proxy2.indeed.com:8000",
        "http://proxy3.indeed.com:8000",
    ]

    def process_request(self, request, spider):
        proxy = random.choice(self.proxies)
        request.meta["proxy"] = proxy
