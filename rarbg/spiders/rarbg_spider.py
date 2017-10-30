import scrapy
import logging
from ..items import Torrent


LOGGER = logging.getLogger(__name__)


class TorrentSpider(scrapy.Spider):
    name = "rarbg"
    # URL of movie torrents sorted by seeders descending order
    start_urls = ['http://rarbg.to/torrents.php?category=14;17;42;44;45;46;47;48;50;51;52&search=&order=seeders&by=DESC']

    def parse(self, response):
        for page_url in response.css('#pager_links > a::attr(href)').extract():
            page_url = response.urljoin(page_url)
            yield scrapy.Request(url=page_url, callback=self.parse)

        for tr in response.css('tr.lista2'):
            tds = tr.css('td')
            yield Torrent(
                title=tds[1].css('a')[0].css('::attr(title)').extract_first(),
                url=response.urljoin(tds[1].css('a')[0].css('::attr(href)').extract_first()),
                date=tds[2].css('::text').extract_first(),
                size=tds[3].css('::text').extract_first(),
                seeders=int(tds[4].css('::text').extract_first()),
                leechers=int(tds[5].css('::text').extract_first()),
                uploader=tds[7].css('::text').extract_first()
            )
