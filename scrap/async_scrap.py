from parsel import Selector
import httpx
import asyncio


class AsyncScraper:
    PLUS_URL = 'https://rezka.ag/'
    URL = 'https://rezka.ag/page/{page}/'
    HEADERS = {
        "Accept-Language":
            "en-GB,en;q=0.5",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0"
    }

    LINK_XPATH = '//div[@class="b-content__inline_item"]/div[@class="b-content__inline_item-link"]/a/@href'
    IMG_XPATH = '//div[@class="b-content__inline_item-cover"]/a/img/@src'
    TITLE_XPATH = '//div[@class="b-content__inline_item-link"]/a/text()'
    DESCRIPTION_XPATH = '//div[@class="b-content__inline_item-link"]/div/text()'

    async def fetch_page(self, client, page):
        try:
            url = self.URL.format(page=page)
            response = await client.get(url, timeout=10.0)
            # print(f"Страница: {page}")

            if response.status_code == 200:
                return Selector(text=response.text)
            else:
                pass
                # response.raise_status()
        except httpx.ReadTimeout:
            print(f"ReadTimeoutError on page: {page}")
            return None

    async def scrape_page(self, selector):
        fresh_links = selector.xpath(self.LINK_XPATH).getall()
        links = [i for i in fresh_links if i.startswith('https://rezka.ag/')]
        images = selector.xpath(self.IMG_XPATH).getall()
        titles = selector.xpath(self.TITLE_XPATH).getall()
        descs = selector.xpath(self.DESCRIPTION_XPATH).getall()
        return_data = []
        for i in range(0, len(links)):
            data = {}
            data['link'] = links[i]
            data['image'] = images[i]
            data['title'] = titles[i]
            data['desc'] = descs[i]
            return_data.append(data)

        return return_data
        # print(links)
        # print(images)

    async def get_pages(self, limit=100):
        async with httpx.AsyncClient(headers=self.HEADERS) as client:
            tasks = [self.fetch_page(client=client, page=page) for page in range(1, limit + 1)]
            pages = await asyncio.gather(*tasks)
            scrape_tasks = [self.scrape_page(page) for page in pages if page is not None]
            return await asyncio.gather(*scrape_tasks)


if __name__ == "__main__":
    scraper = AsyncScraper()
    for i in asyncio.run(scraper.get_pages()):
    # print(asyncio.run(scraper.get_pages()))
        print(i)