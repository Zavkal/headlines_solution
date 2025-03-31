import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

from bs4 import BeautifulSoup

from aiohttp import ClientSession
import asyncio


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
    @staticmethod
    async def parse_kommersant() -> None:
        client = NewsClient()
        for category_id in range(2, 10):
            url = f"https://www.kommersant.ru/archive/rubric/{category_id}/day"

            html_text = await client.fetch_and_read_html_requests(url)

            soup = BeautifulSoup(html_text, "html.parser")
            article_elements = soup.find_all("article", class_="uho rubric_lenta__item js-article")

            for element in article_elements:
                title = element["data-article-title"]
                date = element.find("p", class_="uho__tag").get_text(strip=True)
                article_link = element.find("a", class_="uho__link uho__link--overlay")['href']

        await client.close_session_aiohttp()


    @staticmethod
    async def parse_bloomberg() -> None:
        url = "https://www.bloomberg.com/lineup-next/api/stories?limit=25&pageNumber=1&types=ARTICLE,FEATURE,INTERACTIVE,LETTER,EXPLAINERS"
        session_selenium = SeleniumFetcher()
        response = await session_selenium.fetch_and_read_html_selenium(url)
        soup = BeautifulSoup(response, "html.parser")
        pre_tag = soup.find("pre")
        json_data = json.loads((pre_tag.get_text(strip=True)))
        for data in json_data:
            headline = data.get('headline')
            url_headline = data.get('url')
            date_publ = data.get('publishedAt')



    @staticmethod
    async def parse_reuters() -> None:
        session_selenium = SeleniumFetcher()
        url='https://www.reuters.com/pf/api/v3/content/fetch/articles-by-section-alias-or-id-v1?query={"offset":0,"section_id":"/world/","size":20,"uri":"/world/","website":"reuters"}&d=275&mxId=00000000&_website=reuters'
        response = await session_selenium.fetch_and_read_html_selenium(url)
        soup = BeautifulSoup(response, "html.parser")
        pre_tag = soup.find("pre")
        json_data = json.loads((pre_tag.get_text(strip=True)))
        json_data = json_data.get('result').get('articles')
        for data in json_data:
            headline = data.get('title')
            url_headline = data.get('canonical_url')
            date_publ = data.get('display_time')





async def main():
    parser = ParsNews()
    await parser.parse_reuters()


if __name__ == '__main__':
    asyncio.run(main())