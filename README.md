Here’s a detailed `README.md` for the **Cloud-Native-ETL-Pipeline-Batch-Streaming-Data-Processing** project, structured to explain the setup, usage, and the batch pipeline:

---

# Cloud-Native ETL Pipeline: Batch & Streaming Data Processing

This repository demonstrates how to build a **Cloud-Native ETL Pipeline** using **Apache Airflow**, **Google Cloud Platform (GCP)** services, and **Docker** to handle both **batch** and **real-time (streaming)** data processing.

## Project Overview

The project consists of a **batch ETL pipeline** that pulls cryptocurrency data from the **CoinGecko API**, performs transformations, and loads the data into **BigQuery**. Additionally, a **streaming pipeline** will later be added, which will push changes from BigQuery to **Pub/Sub**, and then process the data in real-time through **Cloud Functions**.

---

## Folder Structure

The directory structure is as follows:

```
Cloud-Native-ETL-Pipeline-Batch-Streaming-Data-Processing/
├── .env                  # Environment variables for local setup
├── .env.example          # Example .env file to be copied and customized
├── .gitignore            # Git ignore file
├── LICENSE               # Project license
├── README.md             # Project documentation
├── docker-compose.yaml   # Docker Compose file to start Airflow environment
├── requirements.txt      # Required Python dependencies for the project
├── start.sh              # Script to start Docker containers
├── airflow/              
│   ├── dags/             # Airflow DAGs for batch ETL pipeline
│   │   ├── coingecko_batch_dag.py  # Main Airflow DAG file
│   │   └── __pycache__/  # Compiled Python files
│   ├── keys/             # GCP service account keys
│   │   └── service-account-key.json  # Service account key for GCP access
│   ├── logs/             # Airflow logs for DAG runs
│   │   ├── dag_id=coingecko_etl_dag/
│   │   │   ├── run_id=.../
│   ├── plugins/          # Airflow custom plugins (if any)
```

---

## Technologies Used

- **Apache Airflow**: Orchestrates the ETL pipeline and scheduling
- **Google Cloud Platform (GCP)**:
  - **BigQuery**: Stores the processed cryptocurrency data
  - **Cloud Storage**: Stores intermediate datasets (if needed)
  - **Google Cloud SDK**: For deploying and managing GCP resources
- **CoinGecko API**: Data source for cryptocurrency market information
- **Docker**: For containerized local setup of Airflow

---

## Prerequisites

To run this project locally, make sure you have the following:

- **Docker** and **Docker Compose** installed on your machine
- **Python 3.8+** installed locally
- A **Google Cloud Platform** account with access to BigQuery and **Service Account Key** credentials
- **Airflow** dependencies installed (if you need to run it outside Docker)

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/utkrashh/Cloud-Native-ETL-Pipeline-Batch-Streaming-Data-Processing.git
cd Cloud-Native-ETL-Pipeline-Batch-Streaming-Data-Processing
```

### 2. Set Up Environment Variables

Create a `.env` file by copying the `.env.example` file:

```bash
cp .env.example .env
```

Update the `.env` file with your own credentials and details for GCP, BigQuery, and your project configuration.

### 3. Install Dependencies

Install the required Python dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Configure Airflow Docker Environment

To set up Airflow using Docker, we use `docker-compose.yaml` to configure services like **Postgres**, **Redis**, and **Airflow** itself.

### 5. Start Airflow Using Docker

Run the following command to start the entire environment:

```bash
docker-compose up --build
```

This will set up:
- **Airflow Webserver** running on port `8080`
- **Airflow Scheduler** for task orchestration
- **Postgres** as the backend database for Airflow
- **Redis** as the broker for Airflow task queues

### 6. Access Airflow UI

Once the Docker containers are up, you can access the Airflow UI at [http://localhost:8080](http://localhost:8080). Use the default credentials (`airflow/airflow`).

### 7. Running the DAG

- Airflow will automatically pick up the DAG file `coingecko_batch_dag.py` from the `airflow/dags/` folder.
- You can manually trigger the DAG or let it run on the schedule defined (every 2 minutes in your case).
- The DAG will:
  1. Check if the BigQuery table exists, and create it if necessary.
  2. Fetch cryptocurrency data from CoinGecko.
  3. Transform and insert the data into BigQuery.

---

## GCP Setup

### 1. Create a Service Account

- In the Google Cloud Console, go to **IAM & Admin** > **Service Accounts**.
- Create a new service account with **BigQuery Admin** and **Storage Admin** roles.
- Download the **JSON Key** and place it in the `airflow/keys/` folder as `service-account-key.json`.

### 2. Configure GCP Credentials in Airflow

Update your `.env` file with the appropriate GCP project details:

```
GCP_PROJECT_ID=your-project-id
BQ_DATASET_ID=your-dataset-id
BQ_TABLE_ID=your-table-id
GOOGLE_APPLICATION_CREDENTIALS=airflow/keys/service-account-key.json
```

---

## Airflow DAGs

### 1. **coingecko_batch_dag.py**

The main DAG script for this batch ETL pipeline is located in `airflow/dags/coingecko_batch_dag.py`. The key components are:

- **create_bigquery_table()**: Checks if the target table exists in BigQuery and creates it if necessary.
- **fetch_coingecko_data()**: Fetches real-time cryptocurrency data from the CoinGecko API.
- **transform_and_insert_data()**: Transforms the data and inserts it into BigQuery.

---

## Running the Batch ETL Pipeline

- The DAG is set to run every 2 minutes based on the schedule defined in `coingecko_batch_dag.py`.
- It will extract data, transform it, and load it into BigQuery.

---

## .env.example

The `.env.example` file contains placeholders for environment variables you need to set up. You should copy this file to `.env` and replace the placeholders with your own values.

Example `.env` file content:

```plaintext
GCP_PROJECT_ID=your_project_id
BQ_DATASET_ID=your_dataset_id
BQ_TABLE_ID=your_table_id
GOOGLE_APPLICATION_CREDENTIALS=airflow/keys/service-account-key.json
```

---

## Troubleshooting

- If the BigQuery table already exists, the DAG will skip the creation step.
- If the DAG fails, check the **Airflow logs** in the `logs/` directory for detailed error messages.

---

## License

This project is licensed under the MIT License.

---

Let me know if you need any adjustments or additional details!