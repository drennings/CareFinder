import scrapy
import json_lines

class DocSpider(scrapy.Spider):
    name = "doctext"
    start_urls = []
    with open('C:\\Users\\Ron\\git\\docSpider\\nnames.jl', 'rb') as f:
            for item in json_lines.reader(f):
                start_urls.append(item['url'])
    

    def parse(self, response):
        
        doc = response.css('body')
        with open('C:\\Users\\Ron\\git\\docSpider\\nnames.jl', 'rb') as f:
            for item in json_lines.reader(f):
                if response.url == item['url']:
                    names = item['result']['PERSON']
        
        for name in names:
            print(name)
            yield {
                'name': name,                    
                'text': (doc.xpath('//*[contains(text(), "'+ name +'")]/../../*/*/text()').extract()),
                'url': response.url

            }

#        next_page = response.xpath('.//a[contains(@class, "header")]/@href').extract_first()
#        if next_page is not None:
#            next_page = response.urljoin(next_page)
#            yield scrapy.Request(next_page, callback=self.parse)