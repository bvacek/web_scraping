import scrapy

class RCPSpider(scrapy.Spider):
    name = 'rcp'

    start_urls = [
                'https://www.realclearpolitics.com/2018/12/11',
            ]

    FEED_EXPORT_FIELDS = ['date(YYYY/MM/DD)', 'title', 'source','author', 'link']

    def parse(self, response):
        date = response.url[-11:-1]
        for post in response.css('div.post'):
            link = post.css('div.title a::attr(href)').extract_first()
            title = post.css('div.title a::text').extract_first()
            author = post.css('div.byline a::text').extract_first()
            source = post.css('div.byline span.source::text').extract_first()
            yield {
                    'date':date,
                    'title':title,
                    'source':source,
                    'author':author,
                    'link':link
                    }

        next_page = response.css('div.article_date_top a::attr(href)').extract_first()
        if next_page is not None and next_page is not '/2017/12/31':
            yield response.follow(next_page, callback=self.parse)
