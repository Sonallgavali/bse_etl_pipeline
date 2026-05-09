import os
import requests
import zipfile
from datetime import datetime, timedelta

DOWNLOAD_FOLDER = "/opt/airflow/data"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

start_date = datetime.today() - timedelta(days=365)
end_date = datetime.today()

headers = {
    "User-Agent": "Mozilla/5.0"
}

current_date = start_date

while current_date <= end_date:

    day = current_date.strftime("%d")
    month = current_date.strftime("%m")
    year_short = current_date.strftime("%y")

    zip_filename = f"EQ{day}{month}{year_short}_CSV.ZIP"

    url = (
        f"https://www.bseindia.com/download/BhavCopy/Equity/{zip_filename}"
    )

    zip_path = os.path.join(DOWNLOAD_FOLDER, zip_filename)

    print(f"Trying: {url}")

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        if response.status_code == 200:

            with open(zip_path, "wb") as file:
                file.write(response.content)

            print(f"Downloaded: {zip_filename}")

            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(DOWNLOAD_FOLDER)

                print(f"Extracted: {zip_filename}")

            except zipfile.BadZipFile:
                print(f"Invalid ZIP file: {zip_filename}")

        else:
            print(f"Not Available: {zip_filename}")

    except Exception as e:
        print(f"Error: {e}")

    current_date += timedelta(days=1)

print("BhavCopy download completed.")
