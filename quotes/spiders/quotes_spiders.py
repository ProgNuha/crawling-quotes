import scrapy
from ..items import QuotesItem

class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    number_page = 2
    start_urls = [
        'http://quotes.toscrape.com/'
    ]

    def parse(self, response):

        items = QuotesItem()

        all_quotes = response.css('div.quote')
        
        for quotes in all_quotes:
            title = quotes.css('span.text::text').extract()
            author = quotes.css('.author::text').extract()
            tag = quotes.css('.tag::text').extract()

            items['title'] = title
            items['author'] = author
            items['tag'] = tag

            yield items

        next_page = 'http://quotes.toscrape.com/page/'+ str(QuoteSpider.number_page) +'/'

        if QuoteSpider.number_page <= 10:
            QuoteSpider.number_page += 1
            yield response.follow(next_page, callback = self.parse)