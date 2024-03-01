import requests
from parsel import Selector


class NewsScraper:
    PLUS_URL = 'https://www.prnewswire.com'
    URL = 'https://www.prnewswire.com/news-releases/news-releases-list/?page=1&pagesize=25'
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

    def scrape_data(self):
        response = requests.request(method="GET", url=self.URL, headers=self.HEADERS)
        # print(response.text)
        tree = Selector(text=response.text)
        links = tree.xpath(self.LINK_XPATH).getall()
        images = tree.xpath(self.IMG_XPATH).getall()
        titles = tree.xpath(self.TITLE_XPATH).getall()
        descs = tree.xpath(self.DESCRIPTION_XPATH).getall()

        for desc in descs:
            print(desc)

        return links


if __name__ == "__main__":
    scraper = NewsScraper()
    scraper.scrape_data()

num = 123
print(num)
