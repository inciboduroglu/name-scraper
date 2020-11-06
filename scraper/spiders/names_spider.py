import scrapy


class NamesSpider(scrapy.Spider):
    name = "names"

    def start_requests(self):
        urls = [
            # "https://www.behindthename.com/names/list",
            # "https://www.behindthename.com/names/usage/eastern-african",
            "https://www.behindthename.com/names/usage/hebrew"
            # "https://www.behindthename.com/name/ada"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_usage)

    def parse(self, response):
        usages = response.css(".usagelist a::attr(href)").getall()
        yield from response.follow_all(usages, callback=self.parse_usage)

    def parse_usage(self, page_response):
        names = page_response.css(".listname a::attr(href)").getall()

        yield from page_response.follow_all(names, callback=self.parse_name)
        # next page
        pages = page_response.xpath('//*[(@id = "div_pagination")]//a/@href')
        yield from page_response.follow_all(pages, callback=self.parse_usage)

    def parse_name(self, name_response):
        name_info = {
            'name': name_response.css(".namebanner-title::text").get(),
            'usage': name_response.css(".usg::text").getall(),
            'related-names': []
        }
        related_page = name_response.css(".nametab_long::attr(href)").get()
        reqqy = name_response.follow(related_page, callback=self.parse_related_names)
        reqqy.meta['item'] = name_info
        return reqqy

    def parse_related_names(self, related_response):
        main = related_response.meta["item"]
        related_sections = related_response.xpath('//div[@class="related-section"]')

        for relsec in related_sections:
            usage = relsec.xpath(".//b/text()").get()
            names = relsec.xpath('.//a[@class="ngl"]/text()').getall()
            rel_name_detail = {
                'usage': usage,
                'names': names
            }

            main['related-names'].append(rel_name_detail)

        return main
