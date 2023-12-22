# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime


def convert_date(date_str):
    # Mapping of French month names to English
    french_to_english = {
        "janvier": "January",
        "février": "February",
        "mars": "March",
        "avril": "April",
        "mai": "May",
        "juin": "June",
        "juillet": "July",
        "août": "August",
        "septembre": "September",
        "octobre": "October",
        "novembre": "November",
        "décembre": "December",
    }

    # Try English format
    try:
        return datetime.strptime(date_str, "%B %d, %Y").date()
    except ValueError:
        pass

    # Replace French month names with English equivalents
    for fr, en in french_to_english.items():
        date_str = date_str.replace(fr, en)

    # Try parsing again after replacement
    try:
        return datetime.strptime(date_str, "%d %B %Y").date()
    except ValueError:
        return date_str


class ReviewScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Clean company name

        company = adapter.get("company")
        if company != None and "Employee Reviews" in company:
            clean_company = company.split("Employee Reviews")[0].strip()
            adapter["company"] = clean_company
        elif company != None and "Working at" in company:
            clean_company = company.split(":")[0].split("at ")[-1].strip()
            adapter["company"] = clean_company
        else:
            adapter["company"] = company

        # remove white space from all strings
        field_names = adapter.field_names()
        for field in field_names:
            if adapter[field] != None:
                if field in ["company", "title", "location", "job_role", "job_status"]:
                    value = adapter.get(field)
                    adapter[field] = value.strip()

                if field in [
                    "work_balance",
                    "benefits",
                    "security_adv",
                    "management",
                    "culture",
                ]:
                    value = adapter.get(field)
                    if value != None:
                        clean_sub_rating = value.strip()[0:3]
                        adapter[field] = float(clean_sub_rating)
                    else:
                        adapter[field] = None

        # remove () from job status
        job_status = adapter.get("job_status")
        clean_job_status = job_status[1:-1]
        adapter["job_status"] = clean_job_status

        # convert rating to float
        rating = adapter.get("rating")
        adapter["rating"] = float(rating[0])

        # convert date
        convert_date
        date = adapter.get("date")
        adapter["date"] = convert_date(date)

        return item
