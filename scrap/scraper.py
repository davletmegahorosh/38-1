import requests
from parsel import Selector


class NewsScraper:
    # PLUS_URL = 'https://www.prnewswire.com/'
    URL = 'https://rezka.ag/'
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


    def scrape_data(self):
        response = requests.request(method="GET", url=self.URL, headers=self.HEADERS)
        # print(response.text)
        tree = Selector(text=response.text)
        fresh_links = tree.xpath(self.LINK_XPATH).getall()
        links = [i for i in fresh_links if i.startswith('https://rezka.ag/')]
        images = tree.xpath(self.IMG_XPATH).getall()
        titles = tree.xpath(self.TITLE_XPATH).getall()
        descs = tree.xpath(self.DESCRIPTION_XPATH).getall()
        return_data = []
        for i in range(0, len(links)):
            data = {}
            data['link'] = links[i]
            data['image'] = images[i]
            data['title'] = titles[i]
            data['desc'] = descs[i]
            return_data.append(data)
        return return_data

if __name__ == "__main__":
    scraper = NewsScraper()
    print(scraper.scrape_data())

