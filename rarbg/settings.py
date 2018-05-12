
BOT_NAME = 'rarbg'

SPIDER_MODULES = ['rarbg.spiders']
NEWSPIDER_MODULE = 'rarbg.spiders'

LOG_LEVEL = 'INFO'
LOG_SHORT_NAMES = True
FEED_EXPORT_INDENT = 4

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko)' \
             ' Chrome/27.0.1453.93 Safari/537.36'

ROBOTSTXT_OBEY = False


DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
    'rarbg.middlewares.ThreatDefenceRedirectMiddleware': 600,
}

CONCURRENT_REQUESTS = 2

# DOWNLOAD_DELAY = 4

COOKIES_ENABLED = True

