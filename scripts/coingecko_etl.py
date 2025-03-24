# scripts/coingecko_etl.py
import requests
import pandas as pd
from google.cloud import bigquery
from datetime import datetime

# Define the ETL function
def run_etl():
    # Step 1: Extract
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
    }
    response = requests.get(url, params=params)
    crypto_data = response.json()

    # Step 2: Transform - Create DataFrame and add timestamp
    df = pd.DataFrame(crypto_data)
    df["timestamp"] = datetime.now()

    # Keep only relevant columns
    df = df[["timestamp", "id", "name", "symbol", "current_price", "market_cap", "price_change_24h"]]

    # Step 3: Load - Append data to BigQuery table
    client = bigquery.Client()
    table_id = "your_project_id.your_dataset_id.crypto_prices"

    # Define load job config
    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("timestamp", "TIMESTAMP"),
            bigquery.SchemaField("id", "STRING"),
            bigquery.SchemaField("name", "STRING"),
            bigquery.SchemaField("symbol", "STRING"),
            bigquery.SchemaField("current_price", "FLOAT"),
            bigquery.SchemaField("market_cap", "FLOAT"),
            bigquery.SchemaField("price_change_24h", "FLOAT"),
        ],
        write_disposition="WRITE_APPEND",  # Append data to the table
    )

    # Load DataFrame into BigQuery
    client.load_table_from_dataframe(df, table_id, job_config=job_config)
    print(f"Data loaded successfully into {table_id}")
