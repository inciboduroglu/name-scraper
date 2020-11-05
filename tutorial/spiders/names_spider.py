import scrapy


class NamesSpider(scrapy.Spider):
    name = "names"

    def start_requests(self):
        urls = [
            # "https://www.behindthename.com/names/list",
            "https://www.behindthename.com/names/usage/eastern-african",
            "https://www.behindthename.com/names/usage/english"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_usage)

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
            'related-names': self.parse_related_names(name_response.follow(".nametab_long::attr(href)"))

            # 'description':
        }

    def parse_related_names(self, related_names_response):
        related_names = related_names_response.css(".related-section").getall()
