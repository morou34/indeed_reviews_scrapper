# Indeed Reviews Scraper

This repository contains a Python script for scraping reviews of one or more companies on Indeed.com.

## Step 1: Installation

- Ensure you have Python installed on your system.
- Clone this repository to your local machine.
- Install the required packages using the following command:

  ```bash
  pip install -r requirements.txt

  ```

- Activate your virtual environment (venv).

## Step 2: Setup Your ScrapeOps Account

This project uses ScrapeOps as a premium proxy provider to avoid blocking our spiders. ScrapeOps offers a free tier suitable for learning or small-scale scraping (e.g., 1000 API credits). After creating your ScrapeOps account, navigate to settings and retrieve your API key. Replace the existing API key in settings.py with your key:

```bash
    SCRAPEOPS_API_KEY = 'your_api_key'
```

## Step 3: Set Up the Companies to Scrape

- Add links to the companies whose reviews you want to scrape in the companies.txt file located in the root directory.
- Format the links as follows:

```bash
https://www.indeed.com/cmp/Delta-Air-Lines/reviews
https://www.indeed.com/cmp/Google/reviews
```

You can add as many links as you need, one per line.

## Step 4: Start the Scraping

Run the scraper using the command:

```bash
python main.py
```

The script will scrape reviews for all listed companies and output one CSV file per company in the companies_links folder.

## Step 5: Merge Reviews (Optional)

If you want to consolidate all reviews into a single file, run:

```bash
python merge_reviews.py
```

A new file named all_reviews_date.csv will be created.

## Note

- The scraper processes the links of the companies one by one. If it stops during the scraping of a specific company, simply run it again, and it will resume from that company. However, it will start from the first review of that company.
- The script removes the links from companies.txt as they are scraped. By the end of the process, companies.txt will be empty. You can modify this behavior if needed.
