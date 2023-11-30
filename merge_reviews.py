import os
import csv
from datetime import datetime
from utils import date_for_filename

input_directory = "companies_reviews"
output_directory = "merged_reviews"


def merge_csv_files(output_folder):
    # Ensure the output directory exists
    if not os.path.exists(input_directory):
        print("No reviews to merge, please run the scrapper first ... ")
        return
    else:
        all_files = os.listdir(output_folder)
        csv_files = [f for f in all_files if f.endswith(".csv")]
        if len(csv_files) < 1:
            print("No files to merge ...")
            return

    # Get current date
    current_date = date_for_filename()  # Format: YYYYMMDD
    merged_filename = f"all_reviews_{current_date}.csv"  # New filename with date
    merged_filename = os.path.join(output_directory, merged_filename)

    with open(merged_filename, "w", newline="", encoding="utf-8") as merged_file:
        writer = None
        for i, filename in enumerate(csv_files):
            with open(
                os.path.join(output_folder, filename), "r", newline="", encoding="utf-8"
            ) as file:
                reader = csv.reader(file)
                rows = list(reader)

                if len(rows) == 0:
                    # Skip empty files
                    continue

                if i == 0:
                    # Write header from the first non-empty file
                    writer = csv.writer(merged_file)
                    writer.writerow(rows[0])
                # Write the data
                for row in rows[1:]:  # Skip the header row for all files
                    writer.writerow(row)


merge_csv_files(input_directory)
