from bs4 import BeautifulSoup
from bs4.element import Tag

import re, uuid, logging
from datetime import datetime

import scrapy
from imdb.items import CastItem

# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor

logger = logging.getLogger(__name__)

class CastSpider(scrapy.Spider):
    name = 'cast_spider'
    custom_settings = {
        'LOG_FILE': './log/cast.log'
    }

    # for test: range(1, 100, 50)
    # for produce: range(1, 5500, 50)
    start_urls = ["https://www.imdb.com/search/name/?gender=male,female&start={}".format(index) for index in range(1, 5500, 50)]

    overall_process = 0

    def parse(self, response):
        print("fetching page:", self.overall_process)
        self.overall_process += 1
        # handle start_urls
        soup = BeautifulSoup(response.body, 'html.parser')
        domain: str = "https://www.imdb.com"
        for lister_item in soup.select(".lister-item"):
            movie_href = domain + lister_item.select("a")[0]['href'] + '/bio'
            yield scrapy.Request(movie_href, self.parse_detail)

    def parse_detail(self, response):
        cast_item = CastItem()
        soup = BeautifulSoup(response.body, 'html.parser')

        cast_item['id'] = uuid.uuid4().hex.upper()
        cast_item['url'] = str(response.url).replace("?ref_=adv_li_i", "")
        cast_item['timestamp_crawl'] = datetime.now().strftime("%Y-%m-%dT%X")

        # name
        try:
            cast_item['name'] = soup.h3.text.strip()
        except Exception as e:
            logger.error("{}, on name, error:{}".format(str(response.url), str(e)))

        # <table id="overviewTable" class="dataTable labelValueTable">
        overviewtable_tag = soup.select('#overviewTable')[0]

        # overviewtable_tag -> Born
        born_tag = ''
        died_tag = ''
        try:
            for sub_item in overviewtable_tag.children:
                if isinstance(sub_item, Tag):
                    if "Born" in sub_item.text:
                        born_tag = sub_item
                    if "Died" in sub_item.text:
                        died_tag = sub_item
            if born_tag == '':
                date_of_birth = ''
                # raise Exception(" born_tag not exist")
            else:
                birth_data_list = [tag.text for tag in born_tag.select('time')[0].select('a')]
                date_of_birth = ','.join(birth_data_list)
            cast_item['date_of_birth'] = date_of_birth
        except Exception as e:
            logger.error("{}, on date_of_birth, error:{}".format(str(response.url), str(e)))

        place_of_birth = ''
        try:
            if born_tag == '':
                pass
            else:
                for born_subitem in born_tag.find_all("a"):
                    if "place" in str(born_subitem):
                        place_of_birth = born_subitem.text
        except Exception as e:
            logger.error("{}, on place_of_birth, error:{}".format(str(response.url), str(e)))
        cast_item['place_of_birth'] = place_of_birth

        # overviewtable_tag  -> Born -> Died
        if died_tag == '':
            date_of_death = ''
            place_of_death = ''
        else:
            try:
                death_date_list = [tag.text for tag in died_tag.select('time')[0].select('a')]
                date_of_death = ','.join(death_date_list)
            except Exception as e:
                logger.error("{}, on date_of_death, error:{}".format(str(response.url), str(e)))
            try:
                for died_subitem in died_tag.find_all("a"):
                    if "place" in str(died_subitem):
                        place_of_death = died_subitem.text
            except Exception as e:
                logger.error("{}, on place_of_death, error:{}".format(str(response.url), str(e)))

        cast_item['date_of_death'] = date_of_death
        cast_item['place_of_death'] = place_of_death

        # mini_bio
        try:
            mini_bio = str(soup.select(".soda p")[0].text.strip())
        except Exception as e:
            logger.error("{}, on mini_bio, error:{}".format(str(response.url), str(e)))
        cast_item['mini_bio'] = mini_bio

        return cast_item
