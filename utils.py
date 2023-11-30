import os
import sys
import time
import datetime
import argparse
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer
from basic_scrapy_spider.spiders.quotes import QuotesSpider


def date_for_filename():
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    return formatted_datetime


# Function to count script run time
def elapsed_time(duration):
    return str(datetime.timedelta(seconds=duration)).split(".")[0]


# Check is date paased as agrs is valid
def is_valid_date(date_str):
    try:
        # Attempt to convert the string to a datetime object
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


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
