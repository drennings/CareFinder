import scrapy


class DocSpider(scrapy.Spider):
    name = "doctors"
    start_urls = [
        #'http://www.nyp.org/lowermanhattan',
		'https://www.roswellpark.org/directory',
    ]

    def parse(self, response):
        print()
        for doc in response.css('body'):
            yield {
                   'div': ' '.join(doc.xpath('//text()[re:test(., "\w+")]').extract()),
                   'url': response.url
				#'div': doc.css('div').extract_first(),
                # 'text': doc.css('span.text::text').extract_first(),
                # 'author': doc.css('small.author::text').extract_first(),
            }

        next_page = response.xpath('.//a[contains(@class, "header")]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)