import scrapy


class NamesSpider(scrapy.Spider):
    name = "names"

    start_urls = [
        "https://www.behindthename.com/names/usage/italian"
    ]

    def parse(self, response):
        for name in response.css(".listname a::text").getall():
            print(name)
