import json

from datetime import datetime
import pytz

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

from bs4 import BeautifulSoup

from aiohttp import ClientSession

from bot.config import category_kommersnat
from database.repositories.headlines_repo import HeadlinesRepository
from database.repositories.news_sources_repo import NewsSourcesRepository
from database.session import db


class NewsClient:
    def __init__(self):
        self.session_aiohttp = ClientSession()


    async def fetch_and_read_html_requests(self, url: str) -> str:
        async with self.session_aiohttp.get(url) as response:
            return await response.text()


    async def close_session_aiohttp(self):
        await self.session_aiohttp.close()


class SeleniumFetcher:
    def __init__(self):
        self.options = ChromeOptions()

    async def fetch_and_read_html_selenium(self, url: str) -> str:
        # self.options.add_argument("--headless")  # Не хочет обходить автокапчу
        driver = webdriver.Chrome(options=self.options)
        driver.get(url)

        page_html = driver.page_source

        driver.close()

        return page_html



class ParsNews:
    news_sources = NewsSourcesRepository(db=db)
    news_headlines = HeadlinesRepository(db=db)


    @staticmethod
    async def cut_url(url: str) -> str:
        return '/'.join(url.split('/')[:3])


    @staticmethod
    async def convert_date_for_bloomberg_reuters(date_publ: str) -> datetime:
        try:
            utc_time = pytz.utc.localize(datetime.strptime(date_publ, "%Y-%m-%dT%H:%M:%SZ"))
        except ValueError:
            utc_time = pytz.utc.localize(datetime.strptime(date_publ, "%Y-%m-%dT%H:%M:%S.%fZ"))
        moscow_time = utc_time.astimezone(pytz.timezone("Europe/Moscow"))
        moscow_time = moscow_time.replace(tzinfo=None)
        return moscow_time


    @classmethod
    async def parse_kommersant(cls) -> list:
        client = NewsClient()
        kommersant_list = []
        try:
            for category_id, value in category_kommersnat.items():
                url = f"https://www.kommersant.ru/archive/rubric/{category_id}/day"
                base_url = await cls.cut_url(url)
                source_id = await cls.news_sources.get_source_id(base_url)
                html_text = await client.fetch_and_read_html_requests(url)

                soup = BeautifulSoup(html_text, "html.parser")
                article_elements = soup.find_all("article", class_="uho rubric_lenta__item js-article")

                for element in article_elements:
                    title = element["data-article-title"]
                    date_publ = element.find("p", class_="uho__tag").get_text(strip=True)
                    article_link = base_url + element.find("a", class_="uho__link uho__link--overlay")['href']
                    date_obj = datetime.strptime(date_publ, "%d.%m.%Y, %H:%M")
                    async with db.session():
                        kommersant_list.append(await cls.news_headlines.create_news(title=title,
                                                             url=article_link,
                                                             date_published=date_obj,
                                                             source_id=source_id,
                                                             category=value))
        finally:
            await client.close_session_aiohttp()
            return kommersant_list


    @classmethod
    async def parse_bloomberg(cls) -> list:
        bloomberg_list = []
        url = "https://www.bloomberg.com/lineup-next/api/stories?limit=25&pageNumber=1&types=ARTICLE,FEATURE,INTERACTIVE,LETTER,EXPLAINERS"
        base_url = await cls.cut_url(url)
        session_selenium = SeleniumFetcher()
        response = await session_selenium.fetch_and_read_html_selenium(url)
        soup = BeautifulSoup(response, "html.parser")
        pre_tag = soup.find("pre")
        json_data = json.loads((pre_tag.get_text(strip=True)))

        source_id = await cls.news_sources.get_source_id(base_url)
        category = 'world'

        for data in json_data:
            headline = data.get('headline')
            url_headline = base_url + data.get('url')
            date_publ = data.get('publishedAt')
            moscow_time = await cls.convert_date_for_bloomberg_reuters(date_publ)
            async with db.session():
                bloomberg_list.append(await cls.news_headlines.create_news(title=headline ,
                                                     url=url_headline,
                                                     date_published=moscow_time,
                                                     source_id=source_id,
                                                     category=category))

        return bloomberg_list


    @classmethod
    async def parse_reuters(cls) -> list:
        reuters_list = []
        url='https://www.reuters.com/pf/api/v3/content/fetch/articles-by-section-alias-or-id-v1?query={"offset":0,"section_id":"/world/","size":20,"uri":"/world/","website":"reuters"}&d=275&mxId=00000000&_website=reuters'
        base_url = await cls.cut_url(url)
        session_selenium = SeleniumFetcher()
        response = await session_selenium.fetch_and_read_html_selenium(url)
        soup = BeautifulSoup(response, "html.parser")
        pre_tag = soup.find("pre")
        json_data = json.loads((pre_tag.get_text(strip=True)))
        json_data = json_data.get('result').get('articles')

        source_id = await cls.news_sources.get_source_id(base_url)
        category = 'world'

        for data in json_data:
            headline = data.get('title')
            url_headline = base_url + data.get('canonical_url')
            date_publ = data.get('display_time')
            moscow_time = await cls.convert_date_for_bloomberg_reuters(date_publ)
            async with db.session():
                reuters_list.append(await cls.news_headlines.create_news(title=headline ,
                                                     url=url_headline,
                                                     date_published=moscow_time,
                                                     source_id=source_id,
                                                     category=category))

        return reuters_list

