import scrapy
from scrapy.selector import Selector


class NamesSpider(scrapy.Spider):
    name = "names"

    def start_requests(self):
        urls = [
            # "https://www.behindthename.com/names/list",
            # "https://www.behindthename.com/names/usage/eastern-african",
            # "https://www.behindthename.com/names/usage/english",
            # "https://www.behindthename.com/name/ada",
            "https://www.behindthename.com/name/ada/related"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_related_names)

    def parse(self, response):
        usages = response.css(".usagelist a::attr(href)").getall()
        yield from response.follow_all(usages, callback=self.parse_usage)

    def parse_usage(self, page_response):
        names = page_response.css(".listname a::attr(href)").getall()

        yield from page_response.follow_all(names, callback=self.parse_name)

    def parse_name(self, name_response):
        yield {
            'name': name_response.css(".namebanner-title::text").get(),
            'usage': name_response.css(".usg::text").getall(),
            # 'meaning': name_response.css(".infogroup+ section .namemain+ div").getall(),
            'related-names': self.parse_related_names(name_response)
        }

    def parse_related_names(self, related_names_response):
        related_name = related_names_response.xpath(
            '//*[contains(concat( " ", @class, " " ), concat( " ", "related-section", " " ))]').get()

        yield {
            'usage': Selector(text=related_name).xpath('//b/text()').get(),
            'names': Selector(text=related_name).xpath(
                '//*[contains(concat( " ", @class, " " ), concat( " ", "ngl", " " ))]/text()').getall()
        }
