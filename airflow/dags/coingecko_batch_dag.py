import os
import requests
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
from google.cloud import bigquery

# Read environment variables from the .env file
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
BQ_DATASET_ID = os.getenv("BQ_DATASET_ID")
BQ_TABLE_ID = os.getenv("BQ_TABLE_ID")

# Define dataset and table names
DATASET_NAME = f"{GCP_PROJECT_ID}.{BQ_DATASET_ID}"
TABLE_NAME = f"{DATASET_NAME}.{BQ_TABLE_ID}"

# Base URL of the CoinGecko API
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/coins/markets"

# Default arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
}

dag = DAG(
    "coingecko_etl_dag",
    default_args=default_args,
    description="A DAG for ETL pipeline to load CoinGecko data into BigQuery",
    schedule_interval="*/2 * * * *",
    start_date=days_ago(1),
    catchup=False,
)

# Create BigQuery Dataset (if it doesn't exist)
def create_bigquery_dataset():
    client = bigquery.Client()
    dataset = bigquery.Dataset(DATASET_NAME)
    dataset.location = "US"  # Choose your region

    # Check if the dataset exists and create if necessary
    try:
        client.get_dataset(DATASET_NAME)
        print(f"Dataset {DATASET_NAME} already exists.")
    except Exception:
        print(f"Dataset {DATASET_NAME} does not exist. Creating it now...")
        client.create_dataset(dataset, exists_ok=True)
        print(f"Dataset {DATASET_NAME} created successfully!")

# Create BigQuery Table (if it doesn't exist)
def create_bigquery_table():
    client = bigquery.Client()

    # Schema (with created_date and created_by)
    schema = [
        bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("symbol", "STRING"),
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("current_price", "FLOAT"),
        bigquery.SchemaField("market_cap", "INTEGER"),
        bigquery.SchemaField("created_date", "TIMESTAMP"),
        bigquery.SchemaField("created_by", "STRING"),
    ]

    # Check if the table exists and create it if necessary
    try:
        client.get_table(TABLE_NAME)
        print(f"Table {TABLE_NAME} already exists.")
    except Exception:
        print(f"Table {TABLE_NAME} does not exist. Creating it now...")
        table = bigquery.Table(TABLE_NAME, schema=schema)
        client.create_table(table)
        print(f"Table {TABLE_NAME} created successfully!")


def fetch_coingecko_data():
    # Fetch real-time cryptocurrency data from CoinGecko
    params = {
        "vs_currency": "inr",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": "false",
    }
    response = requests.get(COINGECKO_API_URL, params=params)
    data = response.json()
    return data


def transform_and_insert_data(**context):
    client = bigquery.Client()
    data = context['task_instance'].xcom_pull(task_ids='fetch_data_from_coingecko')

    # Prepare data for insertion
    rows_to_insert = [
        {
            "id": coin["id"],
            "symbol": coin["symbol"],
            "name": coin["name"],
            "current_price": coin["current_price"],
            "market_cap": coin["market_cap"],
            "created_date": datetime.now().isoformat(),
            "created_by": "airflow_batch_script",
        }
        for coin in data
    ]

    # Insert data into BigQuery (append mode)
    errors = client.insert_rows_json(TABLE_NAME, rows_to_insert)
    if not errors:
        print("Data inserted successfully.")
    else:
        print(f"Encountered errors while inserting data: {errors}")

# Task 1: Create BigQuery Dataset
create_dataset_task = PythonOperator(
    task_id="create_bigquery_dataset",
    python_callable=create_bigquery_dataset,
    dag=dag,
)

# Task 2: Create BigQuery Table
create_table_task = PythonOperator(
    task_id="create_bigquery_table",
    python_callable=create_bigquery_table,
    dag=dag,
)

# Task 3: Fetch Data from CoinGecko API
fetch_data_task = PythonOperator(
    task_id="fetch_data_from_coingecko",
    python_callable=fetch_coingecko_data,
    dag=dag,
)

# Task 4: Transform and Insert Data into BigQuery
insert_data_task = PythonOperator(
    task_id="transform_and_insert_data",
    python_callable=transform_and_insert_data,
    op_kwargs={'context': 'context'},
    dag=dag,
)

# Define DAG flow using the >> operator
create_dataset_task >> create_table_task >> fetch_data_task >> insert_data_task
