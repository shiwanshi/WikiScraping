import scrapy
import schedule
import time
from scrapy import cmdline

# This class is a spider for scraping data from wikipedia
class WikiSpider(scrapy.Spider):
    name = "wiki"
    # the starting url for the spider to crawl
    start_urls = ["https://en.wikipedia.org/wiki/Database"]
    # settings for the spider such as user agent, download delay, 
    # and number of concurrent requests
    custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'DOWNLOAD_DELAY': 1,
    'CONCURRENT_REQUESTS': 1,
    'RETRY_TIMES': 3,
    'RETRY_HTTP_CODES': [500, 503, 504, 400, 403, 404, 408],
    'DOWNLOADER_MIDDLEWARES': {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    }
    }
    # parse method that is called when the spider is done crawling
    def parse(self, response):
        # get the title of the page
        title = response.css("title::text").get()
        # get all the paragraphs from the page
        paragraphs = response.css("p::text").getall()
    # Open the file in write mode
        print(title)
        print(paragraphs)
        with open("wiki.txt", "w") as f:
            f.write(title)
            for para in paragraphs:
                f.write(para+"\n")

# function to run the spider
def crawl_wiki():
    cmdline.execute("scrapy runspider WikiSpider.py".split())

# schedule the spider to run every 30 seconds
schedule.every(30).seconds.do(crawl_wiki)

# infinite loop to run the scheduled spider
while True:
    schedule.run_pending()
    time.sleep(1)
