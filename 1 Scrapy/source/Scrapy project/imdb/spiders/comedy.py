from bs4 import BeautifulSoup
import re,uuid,logging
from datetime import datetime

import scrapy
from imdb.items import ComedyItem
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor

logger = logging.getLogger(__name__)

class ComedySpider(scrapy.Spider):
    name = 'comedy_spider'
    custom_settings = {
        'LOG_FILE': './log/comedy.log'
        
    }
    # for test: range(1, 100, 50)
    # for produce: range(1, 5500, 50)
    start_urls = ["https://www.imdb.com/search/title/?genres=comedy&start={}".format(index) for index in range(1, 5500, 50)]
    overall_process = 0

    def parse(self, response):
        print("fetching page:", self.overall_process)
        self.overall_process += 1
        # handle start_urls
        soup = BeautifulSoup(response.body, 'html.parser')
        domain: str = "https://www.imdb.com"
        for lister_item in soup.select(".lister-item"):
            movie_href = domain + lister_item.select("a")[0]['href']
            yield scrapy.Request(movie_href, self.parse_detail)

    def parse_detail(self, response):
        comedy_item = ComedyItem()
        soup = BeautifulSoup(response.body, 'html.parser')
        comedy_item['id'] = uuid.uuid4().hex.upper()
        comedy_item['url'] = str(response.url).replace("?ref_=adv_li_i", "")
        comedy_item['timestamp_crawl'] = datetime.now().strftime("%Y-%m-%dT%X")

        # title
        comedy_item['title'] = re.findall(r"[\w &'.,:?-]+", soup.h1.text)[0]

        # genres
        try:
            genre_divtag = soup.find_all('div','see-more inline canwrap')[-1]
            genre_list = [a.text.strip() for a in genre_divtag.find_all('a')]
            comedy_item['genres'] = genre_list
        except Exception as e:
            logger.error("{}, on genre, error:{}".format(str(response.url),str(e)))

        # detail div
        detail_div_tag = soup.find('div', id='titleDetails')
        # detail div -> language
        language_list = []
        try:
            for sub_item in detail_div_tag.select('div'):
                if "Language" in sub_item.text:
                    language_list = [language.text.strip() for language in sub_item.find_all('a')]
                    break
            comedy_item['languages'] = language_list
        except Exception as e:
            logger.error("{}, on language, error:{}".format(str(response.url),str(e)))

        # detail div -> release date
        release_date = ''
        date_pattern = re.compile(r'\d+\ \w+\ \d{4}|\d{4}')
        try:
            for sub_item in detail_div_tag.select('div'):
                if "Release Date" in sub_item.text:
                    release_date = re.findall(date_pattern, sub_item.text)[0]
                    break
            comedy_item['release_date'] = release_date
        except Exception as e:
            logger.error("{}, on release date, error:{}".format(str(response.url),str(e)))

        # detail div -> budget
        money_pattern = re.compile(r'[\$\d,]+|[\w]{3}[\$\d,]+')
        budget = ''
        try:
            for sub_item in detail_div_tag.select('div'):
                if "Budget" in sub_item.text:
                    budget = re.findall(money_pattern, sub_item.text)[0]
                    break
            comedy_item['budget'] = budget
        except Exception as e:
            logger.error("{}, on budget, error:{}".format(str(response.url),str(e)))

        # detail div -> gross
        gross = ''
        try:
            for sub_item in detail_div_tag.select('div'):
                if "Worldwide Gross" in sub_item.text:
                    gross = re.findall(money_pattern, sub_item.text)[0]
                    break
            comedy_item['gross'] = gross
        except Exception as e:
            logger.error("{}, on gross, error:{}".format(str(response.url), str(e)))

        # detail div -> runtime
        runtime = ''
        try:
            for sub_item in detail_div_tag.select('div'):
                if "Runtime" in sub_item.text:
                    runtime = sub_item.select('time')[0].text
                    break
            comedy_item['runtime'] = runtime
        except Exception as e:
            logger.error("{}, on runtime, error:{}".format(str(response.url), str(e)))

        return comedy_item
