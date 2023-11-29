import os
import csv
from datetime import datetime


output_directory = "companies_links"


def merge_csv_files(output_folder):
    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        print("No reviews to merge, please run the scrapper first ... ")
        return
    else:
        all_files = os.listdir(output_folder)
        csv_files = [f for f in all_files if f.endswith(".csv")]
        if len(csv_files) < 1:
            print("No files to merge ...")
            return

    # Get current date
    current_date = datetime.now().strftime("%Y%m%d")  # Format: YYYYMMDD
    merged_filename = f"all_reviews_{current_date}.csv"  # New filename with date

    with open(merged_filename, "w", newline="", encoding="utf-8") as merged_file:
        writer = None
        for i, filename in enumerate(csv_files):
            with open(
                os.path.join(output_folder, filename), "r", newline="", encoding="utf-8"
            ) as file:
                reader = csv.reader(file)
                if i == 0:
                    # Write header from the first file
                    writer = csv.writer(merged_file)
                    writer.writerow(next(reader))
                else:
                    # Skip the header for subsequent files
                    next(reader)

                # Write the data
                for row in reader:
                    writer.writerow(row)


merge_csv_files(output_directory)
