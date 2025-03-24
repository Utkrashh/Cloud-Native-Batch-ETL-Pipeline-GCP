# dags/coingecko_etl_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from scripts.coingecko_etl import run_etl

# Define default args for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id="coingecko_etl_dag",
    default_args=default_args,
    description="ETL DAG to fetch crypto prices from CoinGecko and load into BigQuery",
    schedule_interval="*/10 * * * *",  # Runs every 10 minutes
    start_date=days_ago(1),  # Start date set to one day before
    catchup=False,
) as dag:

    # Define the PythonOperator to run the ETL process
    run_coingecko_etl = PythonOperator(
        task_id="run_coingecko_etl",
        python_callable=run_etl,  # Refers to the ETL function in `coingecko_etl.py`
    )

    # Task execution order
    run_coingecko_etl
