from aiohttp import ClientSession
import asyncio


class NewsClient:
    def __init__(self):
        self.session = ClientSession()

    async def fetch_and_read_html(self, url: str) -> str:
        async with self.session.get(url) as response:
            return await response.text()

    async def close(self):
        await self.session.close()



if __name__ == '__main__':
    client = NewsClient()
    await client.fetch_and_read_html("")