"""
Date: 22.10.2020
This spider scrapes 1500 headlines and publishing dates of the category "Coronavirus"
published by the German Newspaper "Süddeutsche Zeitung".
Run in terminal with: scrapy crawl covid_spider_sd -o covid_sd.csv
"""

import scrapy

# create a class spider
class CovidSpiderSD(scrapy.Spider):

    # define name and urls to be crawled
    name = 'covid_spider_sd'
    start_urls = ['https://www.sueddeutsche.de/thema/Coronavirus']

    # page number to be incremented
    page = 1

    # this method is used to get all href links from article teaser listings on coronavirus
    def parse(self, response):

        # iterate through article listing
        for post in response.css('div.teaserlist'):

            # iterate through articles
            for article in post.css('a.sz-teaser'):

                # extract href-link of article
                link = article.xpath('@href').get()

                # follow the link to parse headline + date
                yield response.follow(link, self.parse_article)

    # this method parses the article and extracts headline + date
    def parse_article(self, response):

        # find headline and date
        headline = response.xpath('//div/article/header/h2/span/text()')[2].extract()
        date = "".join(response.xpath('//div/article/header/time/text()').extract())
        yield {'Date': date,
               'Headline': headline,
               'Newspaper': 'Süddeutsche Zeitung'
               }

        # increment page by 1
        self.page += 1

        # construct url for next page
        next_page = self.start_urls[0] + '-' + str(self.page)

        # start parsing again
        if next_page is not None:
            yield response.follow(next_page, self.parse)
