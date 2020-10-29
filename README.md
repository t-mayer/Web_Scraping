# Web Scraping
This repository is a collection of web scrapers. The scrapers use different libraries/packages such as Selenium, beautifulsoup, scrapy etc.
The web scrapers focus on scraping various German news websites.


### Generic News Scraper
This crawler scrapes articles from a news website and stores the information in a dataframe. It uses beautifulsoup and Selenium webdriver. Additionally, data cleaning can be performed on the scraped content via Data_Cleaning.py

### Bild Zeitung Scraper
This scraper uses a scrapy spider to crawl headlines and dates of the German news website "Bild". Since Bild does not have a separate category for Coronavirus news, the scraper makes use of the search results on that website. 

### Der Spiegel Scraper
This scraper uses a scrapy spider to crawl headlines and dates of the German news website "Der Spiegel". Again, the focus is on Coronavirus news but the category in the url can be exchanged by a different topic.

### Die Zeit Scraper
This scraper uses a scrapy spider to crawl headlines and dates of the German news website "Die Zeit". 
This scraper is a little bit different than the others because Zeit forces visitors to consent to ads. The consent can be given by using a headless Selenium webdriver. Parsing of the websites is then performed in the typical scrapy-fashion.

### Russia Today Scraper
This scraper uses a scrapy spider to crawl headlines and dates of the German news website "Russia Today". RT is known to distribute fake news, so the scraped content will be interesting to examine.

### Süddeutsche Zeitung
This scraper uses a scrapy spider to crawl headlines and dates of the German news website "Süddeutsche Zeitung". Since Süddeutsche does not list the date in the article listing, the scraper needs to access each href from the listing to retrieve date + headline. Therefore, two parsing methods are used.

# Why is it useful?
The program can not only be used to scrape mainstream media but also 'news' websites that promote fake news. 
Having this information, various NLP tasks (e.g. sentiment analysis, topic modeling) can be performed on the scraped content.
