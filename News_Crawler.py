"""
Date: 10.09.2020
This crawler scrapes articles from a news website and stores the information in a dataframe.
The Website-class is used for specific information about the website architecture while
the Crawler-class accesses the website via TOR and PhantomJS and scrapes a number of articles from a certain category
(e.g. politics, sports).
"""

# import packages, libraries, and set options
from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

pd.set_option('display.max_columns', 10)

# make sure TOR browser is open to run this crawler
# specify that selenium connects through port 9150 and uses SOCKS5 protocol
service_args = ['--proxy=localhost:9150', '--proxy-type=socks5', ]

# use PhantomJS (headless browser), specify path for PhantomJS.exe
driver = webdriver.PhantomJS(executable_path='<Path to PhantomJS.exe>', service_args=service_args)


# common base class to specify news website structure (such as html tags, url, and topic)
class Website:
    def __init__(self, url, title_tag, body_tag, date_tag, more_button_tag, href_link, topics):
        self.url = url
        self.title_tag = title_tag
        self.body_tag = body_tag
        self.date_tag = date_tag
        self.more_button_tag = more_button_tag
        self.href_link = href_link
        self.topics = topics


# Crawler class: accesses specific part of website, finds a number of linked articles for a specific topic (e.g. politics),
# and then crawls them. The output is a dataframe.
class Crawler:


    def access_website(self, url, topic):
        """this method accesses the specific webpage"""

        # merge base url with the specific topic
        topic_url = url + '/' + topic + '/'

        # use selenium webdriver to navigate to the page
        driver.get(topic_url)


    def count_links(self, href_link):
        """this method counts how many article links
         (href) of a specific webpage category are listed"""

        # get the source of the current page and find all href links to articles
        html_source = driver.page_source
        bs = BeautifulSoup(html_source)
        href_links = bs.find_all(class_=href_link)

        # count the links
        count_links = 0
        for link in href_links:
            count_links += 1

        return count_links, href_links


    def get_href_links(self, href_link, more_button_tag):
        """this method allows to access more articles/href_links
        by clicking a 'view more' button"""

        # count available href links
        count_links, href_links = self.count_links(href_link)

        # click 'view more' button
        while True:
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, more_button_tag)))
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, more_button_tag))).click()

            # set how many articles should be crawled
            if count_links > 100:
                break
            else:
                count_links, href_links = self.count_links(href_link)

        return href_links


    def access_article(self, site):
        """this method uses the article links (hrefs) to
        scrape the articles and fill a df with them"""

        # make df to fill with scraped info
        columns = ['News Site', 'Category', 'Article Title', 'Date Published', 'Article']
        df = pd.DataFrame(columns=columns)

        # iterate through the topics/categories
        for topic in site.topics:

            # access specific category page of a news website
            self.access_website(site.url, topic)

            # find article listings to access articles: returns href_links
            articles = self.get_href_links(site.href_link, site.more_button_tag)

            # access each href-link
            for link in articles:
                link = link.get('href')

                req = requests.get(site.url + link)
                article = BeautifulSoup(req.text, 'html.parser')

                # crawl the title: find the heading, the article date,
                # get the text and strip unnecessary white space.
                try:
                    title = article.find(class_=site.title_tag).get_text().strip()
                    body = article.find(class_=site.body_tag).find_all('p')

                    # strip paragraphs of white space and save as list
                    body_paragraphs = [para.text.strip() for para in body]

                    date = article.find(class_=site.date_tag).get_text().strip()

                    # saves the scraped article information in a list
                    scraped_article = [site.url, topic, title, date, body_paragraphs]

                    # fill df row-wise
                    df.loc[len(df)] = scraped_article

                except AttributeError as e:
                    continue

        # Optional: save as csv
        df.to_csv("News.csv")
        return df


# make instance of Crawler class
crawler = Crawler()

# provide information of the news website architecture to an instance of the Website class
website = Website('<main URL>', '<article title tag>', '<article body tag>', '<article date tag>',
                  '<CSS selector for view-more-button>', '<href tag>', '<list of categories>')

# scrape (this process takes a while)
print(crawler.access_article(website))
