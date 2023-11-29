import os
import time
import datetime
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer
from basic_scrapy_spider.spiders.quotes import QuotesSpider


def elapsed_time(duration):
    return str(datetime.timedelta(seconds=duration)).split(".")[0]


# Ensure the output directory exists
output_directory = "companies_reviews"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)


# Function to read URLs from a text file
def get_urls():
    with open("companies.txt", "r") as file:
        urls = [url.strip() for url in file.readlines()]
    return urls


# Function to create a safe filename from a URL
def get_safe_filename(url):
    return url.split("/")[-2]


# Function to update the file by removing the processed URL
def update_file(url, filename="companies.txt"):
    with open(filename, "r") as file:
        urls = file.readlines()
    with open(filename, "w") as file:
        for line in urls:
            if line.strip() != url:
                file.write(line)


# Function to run the spider
@defer.inlineCallbacks
def run_spider(url):
    filename = f"{get_safe_filename(url)}.csv"
    output_path = os.path.join(output_directory, filename)

    settings = get_project_settings()
    settings.set(
        "FEEDS",
        {
            output_path: {
                "format": "csv",
                "encoding": "utf8",
            }
        },
    )

    runner = CrawlerRunner(settings)
    yield runner.crawl(QuotesSpider, url_list=[url])
    update_file(url)
    if url == url_list[-1]:  # Check if it's the last URL
        reactor.stop()


# Function to crawl through each URL
@defer.inlineCallbacks
def crawl(url_list):
    for url in url_list:
        print(f"\n\n\n---------------{url}-----------------------\n")
        yield run_spider(url)


# Main script execution
if __name__ == "__main__":
    start_time = time.time()
    time.sleep(1)
    configure_logging()
    url_list = get_urls()
    if len(url_list):
        crawl_job = crawl(url_list)
        reactor.callWhenRunning(crawl_job.__next__)
        reactor.run()

        end_time = time.time()
        duration = end_time - start_time
        formatted_time = elapsed_time(duration)
        print(f"\n-------> Scrapping is finished ({formatted_time})... \n")
    else:
        print("\nNo companies to scrap *_* ...\n")

    
