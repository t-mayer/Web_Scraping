"""
Date: 22.10.2020
This spider scrapes 1000 headlines and publishing dates of the category "Coronavirus"
published by the German Newspaper "Die Zeit".
Run in terminal with: scrapy crawl covid_spider_zeit -o output_Zeit.csv
"""
import scrapy
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# create a class spider
class CovidSpiderZeit(scrapy.Spider):
    # set spider name and start url
    name = 'covid_spider_zeit'
    start_urls = ['https://www.zeit.de/thema/coronavirus']

    # count for next page
    page = 1

    # execute the request to return response object, and call parse method
    def start_request(self):
        yield scrapy.Request(url=self.start_urls, callback=self.parse)

    # parse the response
    def parse(self, response):

        # the try block uses selenium webdriver to consent to ads
        try:
            # headless driver
            options = Options()
            options.headless = True
            driver = webdriver.Firefox(options=options,
                                       executable_path=r'<Path to geckodriver>')

            # navigate to page given by url
            driver.get(response.url)

            # click on the consent button
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.option__action'))).click()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'span.zon-teaser-standard__title')))

            # use the page_source obtained by driver as response object
            selector = scrapy.Selector(text=driver.page_source)

            # quit driver
            driver.quit()

            # now get the article listings and extract headline + date
            for post in selector.css('div.cp-region.cp-region--standard'):

                for article, date in zip(post.css('span.zon-teaser-standard__title::text'),
                                         post.css("time.zon-teaser-standard__datetime::attr(datetime)")):
                    yield {'Date': date.get(),
                           'Headline': article.get(),
                           'Newspaper': 'Die Zeit'}

            # increment next page
            self.page += 1

            # construct url for next page
            next_page = self.start_urls + '?p=' + str(self.page)

            # call parse method on next page
            if next_page is not None:
                yield scrapy.Request(url=next_page, callback=self.parse)

        # the except block is used when the consent for ads was already given, e.g. when parsing next pages
        except:
            for post in response.css('div.cp-region.cp-region--standard'):

                for article, date in zip(post.css('span.zon-teaser-standard__title::text'),
                                         post.css("time.zon-teaser-standard__datetime::attr(datetime)")):
                    yield {'Date': date.get(),
                           'Headline': article.get(),
                           'Newspaper': 'Die Zeit'}

            self.page += 1

            # construct url for next page
            next_page = self.start_urls[0] + '?p=' + str(self.page)

            if next_page is not None:
                yield scrapy.Request(url=next_page, callback=self.parse)
