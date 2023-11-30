from utils import *


# Ensure the output directory exists
output_directory = "companies_reviews"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)


# Function to run the spider
@defer.inlineCallbacks
def run_spider(url, cut_off_date):
    current_date = date_for_filename()
    filename = f"{get_safe_filename(url)}_{current_date}.csv"
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
    yield runner.crawl(QuotesSpider, url_list=[url], cut_off_date=cut_off_date)
    update_file(url)
    if url == url_list[-1]:  # Check if it's the last URL
        reactor.stop()


# Function to crawl through each URL
@defer.inlineCallbacks
def crawl(url_list, cut_off_date):
    for url in url_list:
        print(f"\n\n\n---------------{url}-----------------------\n")
        yield run_spider(url, cut_off_date)


# Main script execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Indeed Reviews Scraper")
    parser.add_argument(
        "--date",
        type=str,
        help="Cut-off date for reviews in YYYY-MM-DD format",
        required=False,
    )
    args = parser.parse_args()

    cut_off_date = args.date

    if cut_off_date:
        print(
            "Please confirm that you want to collect only reviews posted after:",
            cut_off_date,
        )
        decision = input("Answer (Y/N): ")

        # Exit the script with an error code
        if decision.lower() != "y":
            print("Exiting...")
            sys.exit(0)  # Exit the script
        # Exit the script with an error code
        elif not is_valid_date(cut_off_date):
            print("Invalid date format (YYYY-MM-DD). Exiting...")
            sys.exit(1)

    start_time = time.time()
    configure_logging()
    url_list = get_urls()
    if len(url_list):
        crawl_job = crawl(url_list, cut_off_date)
        reactor.callWhenRunning(crawl_job.__next__)
        reactor.run()

        end_time = time.time()
        duration = end_time - start_time
        formatted_time = elapsed_time(duration)
        print(f"\n-------> Scrapping is finished ({formatted_time})... \n")
    else:
        print("\nNo companies to scrap *_* ...")
        print(
            "Please add the links to companies.txt file and run the script again ...\n"
        )
