# quotes.py
from basic_scrapy_spider.items import QuoteItem
from basic_scrapy_spider.items import ReviewItem
from basic_scrapy_spider.pipelines import convert_date
import scrapy
from .selectors import *
from urllib.parse import urljoin
import dateutil.parser


def find_rating(data, category):
    for item in data:
        if category in item[0].strip().lower():
            return item[1]
    return None


class QuotesSpider(scrapy.Spider):
    name = "reviews"
    allowed_domains = ["indeed.com"]

    def __init__(self, url_list=None, cut_off_date=None, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.start_urls = url_list or []
        self.cut_off_date = (
            dateutil.parser.parse(cut_off_date) if cut_off_date else None
        )
        self.isCutOffActivated = False

    def parse(self, response):
        reviews = response.css(REVIEW_CARD)
        company_name = response.css(COMPANY_NAME_SELECTOR).get()
        review_item = ReviewItem()

        for review in reviews:
            title = review.css(TITLE_SELECTOR).extract_first()

            body_texts = review.css(REVIEW_BODY_SELECTOR).getall()
            body = " ".join(body_texts).strip()

            location = review.css(LOCATION_SELECTOR).extract_first()

            # job info eg: Cashier (Former Employee) - Muskegon, MI - Mars 25, 2023
            job_info = review.css(JOB_INFO_SELECTOR).extract()
            date = job_info[-1].strip() if job_info else None
            collected_date = dateutil.parser.parse(date) if date else None

            if (
                self.cut_off_date
                and collected_date
                and collected_date < self.cut_off_date
            ):
                self.isCutOffActivated = True
                continue

            # Extract the Job title and info
            job_role = review.css(JOB_ROLE_SELECTOR).extract_first()
            job_status = job_info[1].strip()

            # Extracting the ratings. This will yield a list of ratings.
            ratings = review.css(RATING_SELECTOR).extract()
            ratingToolTips = review.css(RATING_TOOL_SELECTOR)
            ratings_tool = []
            for selector in ratingToolTips:
                category_rating = selector.xpath(CATEGORY_RATING_SELECTOR).get()
                category = selector.css(RATING_CATEGORY_SELECTOR).get()

                # Process the extracted data (aria_label and span_text)
                ratings_tool.append((category, category_rating))

            # Handling cases where pros and cons might not exist
            pros_list = []
            cons_list = []

            # Check if the div exists
            pros_cons_div = review.css(CONS_PROS_DIV_SELECTOR)

            if pros_cons_div:
                # Extract the first and second child divs
                pros_div = pros_cons_div.xpath(PROS_SELECTOR)
                cons_div = pros_cons_div.xpath(CONS_SELECTOR)

                # Extract all span texts for Pros
                pros_spans = pros_div.css(PROS_SPANS).getall()
                pros_list.extend(pros_spans)

                # Extract all span texts for Cons
                cons_spans = cons_div.css(CONS_SPANS).getall()
                cons_list.extend(cons_spans)

            review_item["company"] = company_name
            review_item["title"] = title
            review_item["body"] = body
            review_item["date"] = date
            review_item["location"] = location
            review_item["job_role"] = job_role
            review_item["job_status"] = job_status
            review_item["rating"] = ratings
            review_item["work_balance"] = find_rating(ratings_tool, BALANCE_CAT)
            review_item["benefits"] = find_rating(ratings_tool, BENEFITS_CAT)
            review_item["security_adv"] = find_rating(ratings_tool, SECURITY_CAT)
            review_item["management"] = find_rating(ratings_tool, MANAGMENT_CAT)
            review_item["culture"] = find_rating(ratings_tool, CULTURE_CAT)
            review_item["pros"] = pros_list
            review_item["cons"] = cons_list

            yield review_item

        if not self.isCutOffActivated:
            next_page = response.css('li a[data-testid="next-page"]::attr(href)').get()

            if next_page is not None:
                base_url = "https://www.indeed.com"
                next_page_url = urljoin(base_url, next_page)
                print(f"\n\n\n\n------------------->{next_page_url}")
                yield response.follow(next_page_url, callback=self.parse)
