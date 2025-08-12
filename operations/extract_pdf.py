import csv
import re
import requests


from .ai import print_test
from .extract_pdf_info import send_to_ai

def get_data(csv_file_path: str, limit: int = 10):
    with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=";")

        count = 0
        
        for row_number, row in enumerate(reader):
            project = ""
            deliverable = ""
            doi = ""
            pdf_id = ""

            # Skip first row
            if row_number == 0:
                continue

            for col_number, column in enumerate(row):
                if col_number == 0:
                    project = column
                elif col_number == 1:
                    deliverable = column
                elif col_number == 2:
                    doi = column
                    match = re.search(r"(\d+)(?!.*\d)", column)
                    if match:
                        pdf_id = match.group(1)

            pdf = get_pdf(pdf_id)
            print_test(project, deliverable, doi, pdf_id)
            send_to_ai(project, deliverable, doi, pdf)

            count += 1
            if count > 10:
                break

def get_pdf(pdf_id: str):
    pdf_url = f"https://zenodo.org/api/records/{pdf_id}/files-archive"

    try:
        response = requests.get(pdf_url)

        if response.status_code == 200:
            """
            # Save file
            filename = f"{pdf_id}.pdf"
            with open(filename, "wb") as f:
                f.write(response.content)
                print(f"PDF downloaded successfully and saved as '{filename}'")
            """
            return response.content
        else:
            print(f"Failed to download PDF. Status code: {response.status_code}")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
