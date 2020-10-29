"""
Date: 22.10.2020
This spider scrapes 1500 headlines and publishing dates of the category "Coronavirus"
published by the German Newspaper "Der Spiegel".
Run in terminal with: scrapy crawl covid_spider_spiegel -o covid_spiegel.csv
"""

import scrapy


# create a class spider
class CovidSpiderSpiegel(scrapy.Spider):

    # define name and urls to be crawled
    name = 'covid_spider_spiegel'
    start_urls = ['https://www.spiegel.de/thema/coronavirus/']

    # to parse next pages
    page = 1

    # parse the response
    def parse(self, response):

        # parse response according to css-selectors
        for post in response.css('section.bg-white'):  # article listing

            # extract headline and date of each article
            for article, date in zip(post.css('h2.w-full'), post.css('footer.font-sansUI.text-shade-dark.text-s')):

                yield {'Date': date.css('span::text').get(),
                       'Headline': article.css('span.align-middle::text').get(),
                       'Newspaper': 'Der Spiegel'}

            # increment page number
            self.page += 1

            # construct url for next page
            next_page = self.start_urls[0] + 'p' + str(self.page) + '/'

            # parse next page
            if next_page is not None:
                yield response.follow(next_page, self.parse)




