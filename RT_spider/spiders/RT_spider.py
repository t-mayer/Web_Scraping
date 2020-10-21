"""
Date: 27.09.2020
This spider scrapes headlines and publishing dates of a category (e.g. Asia, Economy, Russia)
of the German RT News website. Run in terminal with: scrapy crawl rtspider -o headlines.csv
"""

import scrapy


# create a class spider
class RTSpider(scrapy.Spider):

    # define name and urls to be crawled
    name = 'rtspider'
    start_urls = ['https://deutsch.rt.com/inland/']

    # parse the response
    def parse(self, response):

        # parse response according to css-selectors
        for post in response.css('div.listing__content'):  # article listing

            # extract headline and date of each article
            for article in post.css('div.card '):
                yield {'Headline': article.css('a::text').get(),
                       'Date': article.css('div.card__footer ::text').get()
                       }

        # look for the next-page button
        next_page = response.css('div.button a::attr(data-href)').get()

        # start parsing again
        if next_page is not None:
            yield response.follow(next_page, self.parse)
