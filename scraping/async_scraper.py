from parsel import Selector
import httpx
import asyncio


class AsyncScraper:
    PLUS_URL = 'https://www.prnewswire.com'
    URL = 'https://www.prnewswire.com/news-releases/news-releases-list/?page={page}&pagesize=25'
    HEADERS = {
        "Accept-Language":
            "en-GB,en;q=0.5",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0"
    }

    LINK_XPATH = '//div[@class="row newsCards"]/div[@class="card col-view"]/a/@href'
    IMG_XPATH = '//div[@class="img-ratio-element"]/img/@src'
    TITLE_XPATH = '//div[@class="col-sm-8 col-lg-9 pull-left card"]/h3/text()'
    DESCRIPTION_XPATH = '//p[@class="remove-outline"]/text()'

    async def fetch_page(self, client, page):
        try:
            url = self.URL.format(page=page)
            response = await client.get(url, timeout=10.0)
            print(f"Страница: {page}")

            if response.status_code == 200:
                return Selector(text=response.text)
            else:
                response.raise_status()
        except httpx.ReadTimeout:
            print(f"ReadTimeoutError on page: {page}")
            return None

    async def scrape_page(self, selector):
        links = selector.xpath(self.LINK_XPATH).getall()
        images = selector.xpath(self.IMG_XPATH).getall()
        print(links)
        print(images)

    async def get_pages(self, limit=100):
        async with httpx.AsyncClient(headers=self.HEADERS) as client:
            tasks = [self.fetch_page(client=client, page=page) for page in range(1, limit + 1)]
            pages = await asyncio.gather(*tasks)
            scrape_tasks = [self.scrape_page(page) for page in pages if page is not None]
            await asyncio.gather(*scrape_tasks)


if __name__ == "__main__":
    scraper = AsyncScraper()
    asyncio.run(scraper.get_pages())
