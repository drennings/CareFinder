import scrapy
import json_lines

class DocSpider(scrapy.Spider):
    name = "doctext"
    with open('C:\\Users\\Ron\\git\\docSpider\\names.jl', 'rb') as f:
            for item in json_lines.reader(f):
                url = item['url']
    start_urls = [
	    url,
    ]

    def parse(self, response):
        
        doc = response.css('body')
        #text = ' '.join(doc.xpath('//text()[re:test(., "\w+")]').extract()
        with open('C:\\Users\\Ron\\git\\docSpider\\names.jl', 'rb') as f:
            for item in json_lines.reader(f):
                names = item['result']['PERSON']
        
        for name in names:
            print(name)
            yield {                    
                'text': (doc.xpath('//*[contains(text(), "'+ name +'")]/../../*/*/text()').extract())

            }

        next_page = response.xpath('.//a[contains(@class, "header")]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)