"""
Date: 22.10.2020
This spider scrapes 1000 headlines and publishing dates of each of the categories
"Coronavirus"/"Corona"/"Covid" published by the German Newspaper "Bild".
Run in terminal with: scrapy crawl covid_spider_bild -o covid_bild.csv
"""

import scrapy


# create a class spider
class CovidSpiderSD(scrapy.Spider):
    # define name and urls to be crawled
    name = 'covid_spider_bild'

    # since Bild does not have a separate Coronavirus-category, we will use the search page
    # to retrieve headlines about the virus
    start_urls = ['https://www.bild.de/suche.bild.html?query=corona&resultsPerPage=1000',
                  'https://www.bild.de/suche.bild.html?query=covid&resultsPerPage=1000',
                  'https://www.bild.de/suche.bild.html?query=coronavirus&resultsPerPage=1000']

    # this method is used to get all href links from article listings on coronavirus
    def parse(self, response):

        # iterate through listings
        for post in response.css('li'):
            for article in post.css('div.hentry.landscape.search.t9l'):

                # get headline and date
                yield {'Date': article.css('a::attr(data-tb-title)').get(),
                       'Headline': article.css('time::attr(datetime)').get(),
                       'Newspaper': 'Bild'}
