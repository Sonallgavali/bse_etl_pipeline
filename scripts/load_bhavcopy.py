import pandas as pd
import os
import re
from sqlalchemy import create_engine

# PostgreSQL connection
DB_URI = "postgresql+psycopg2://airflow:airflow@postgres:5432/airflow"

engine = create_engine(DB_URI)

# Data folder
DATA_FOLDER = "/opt/airflow/data"


def extract_trade_date(filename):

    """
    Extract date from filename:
    BhavCopy_BSE_CM_0_0_0_20260402_F_0000.CSV
    """

    match = re.search(r'(\d{8})', filename)

    if match:

        date_str = match.group(1)

        year = date_str[:4]
        month = date_str[4:6]
        day = date_str[6:8]

        return f"{year}-{month}-{day}"

    return None


def process_file(filepath):

    filename = os.path.basename(filepath)

    trade_date = extract_trade_date(filename)

    print(f"\nProcessing File: {filename}")
    print(f"Trade Date: {trade_date}")

    # Read CSV
    df = pd.read_csv(filepath)

    # Standardize column names
    df.columns = [col.strip() for col in df.columns]

    # Select required columns
    df = df[
        [
            'TckrSymb',
            'OpnPric',
            'HghPric',
            'LwPric',
            'ClsPric',
            'TtlTradgVol'
        ]
    ]

    # Rename columns
    df = df.rename(columns={
        'TckrSymb': 'symbol',
        'OpnPric': 'open_price',
        'HghPric': 'high_price',
        'LwPric': 'low_price',
        'ClsPric': 'close_price',
        'TtlTradgVol': 'volume'
    })

    # Add metadata columns
    df['trade_date'] = trade_date
    df['source_file'] = filename

    # Remove null symbols
    df = df[df['symbol'].notna()]

    print(df.head())

    # Load to PostgreSQL
    df.to_sql(
        'stg_bhavcopy',
        engine,
        if_exists='append',
        index=False
    )

    print(f"Loaded {len(df)} rows into stg_bhavcopy")


if __name__ == "__main__":

    files = [
        file for file in os.listdir(DATA_FOLDER)
        if file.endswith(".CSV")
    ]

    if not files:
        print("No CSV files found.")

    for file in files:

        filepath = os.path.join(DATA_FOLDER, file)

        process_file(filepath)

    print("\nAll files processed successfully.")
