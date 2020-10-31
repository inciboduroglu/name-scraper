import scrapy


class NamesSpider(scrapy.Spider):
    name = "names"

    start_urls = [
        "https://www.behindthename.com/names/list"
    ]

    def parse(self, response):
        def parse_page(page_response):
            yield {
                'name': page_response.css(".listname a::text").get(),
                # 'description':
            }

        usages = response.css(".usagelist a::attr(href)").getall()
        for usage in usages:
            print(usage)
            yield response.follow(usage, callback=parse_page)
