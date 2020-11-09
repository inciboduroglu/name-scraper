import scrapy
import Gender
from preprocessor.formatters import format_culture_name


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
        page_name = format_culture_name(page_response.css("h1::text").get())
        names = page_response.css(".listname a::attr(href)").getall()

        yield from page_response.follow_all(names, callback=self.parse_name, meta={'page_name': page_name})
        # next page
        pages = page_response.xpath('//*[(@id = "div_pagination")]//a/@href')
        yield from page_response.follow_all(pages, callback=self.parse_usage)

    def parse_name(self, name_response):
        feminine = name_response.css(".fem").get()
        masculine = name_response.css(".masc").get()
        name_info = {
            'name': name_response.css(".namebanner-title::text").get(),
            'usage': name_response.css(".usg::text").getall(),
            'gender': Gender.get_gender(feminine, masculine),
            'related-names': [],
            'page_name': name_response.meta['page_name']
        }
        related_page = name_response.css(".nametab_long::attr(href)").get()
        if related_page is not None:
            reqqy = name_response.follow(related_page, callback=self.parse_related_names)
            reqqy.meta['item'] = name_info
            return reqqy
        else:
            return name_info

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
