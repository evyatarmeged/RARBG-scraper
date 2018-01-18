from scrapy import crawler
from rarbg.spiders.rarbg_spider import TorrentSpider


def main():
    spider = crawler.CrawlerProcess()
    spider.crawl(TorrentSpider)
    spider.start()


if __name__ == '__main__':
    main()


