# Cloud-Native ETL Pipeline (Batch Data Processing)

This project is a **batch ETL (Extract, Transform, Load) pipeline** built using **Apache Airflow** to ingest cryptocurrency data from the **CoinGecko API** and load it into **Google BigQuery**.

The project is containerized with **Docker Compose** and includes all the necessary configurations to deploy and run the Airflow DAG locally. This guide will walk you through the setup process, including configuring a **service account**, managing environment variables securely, and running the ETL pipeline.

---

## 🚀 Features
- Fetches **real-time cryptocurrency data** from the CoinGecko API.
- Loads data into a **BigQuery table** in **Google Cloud Platform (GCP)**.
- Automatically creates the BigQuery table (if it doesn’t exist) with additional columns for metadata like `created_date` and `created_by`.
- Uses **Docker Compose** to run Apache Airflow (web server, scheduler, Redis, PostgreSQL) locally.

---

## 🛠 Project Directory Structure

```
Cloud-Native-ETL-Pipeline-Batch-Streaming-Data-Processing/
│
├── airflow/                    # Folder for Apache Airflow setup
│   ├── docker-compose.yaml     # Docker Compose file to run Airflow services
│   └── .env                    # Environment variables file (to store sensitive credentials)
│   └── env.example             # Example of the .env file to help others set up their environment
│   |__ dags/                   # Folder to store Airflow DAGs (Directed Acyclic Graphs)
│   └── coingecko_batch_dag.py  # Airflow DAG script for the batch ETL pipeline
│
└── venv/                       # Virtual environment folder (created by Python)
```

---

## 🔧 Setup Instructions

### Step 1: Clone the Repository
```bash
git clone https://github.com/utkrashh/Cloud-Native-ETL-Pipeline-Batch-Streaming-Data-Processing.git
cd Cloud-Native-ETL-Pipeline-Batch-Streaming-Data-Processing
```

---

### Step 2: Configure Environment Variables

To avoid storing sensitive credentials in the code, we use a `.env` file to manage environment variables.

1. **Create the `.env` file:**
   - Copy the `env.example` file and rename it to `.env`:
     ```bash
     cp airflow/env.example airflow/.env
     ```

2. **Edit the `.env` file**:
   - Add your Google Cloud project information:
     ```
     # Google Cloud Credentials
     GCP_PROJECT_ID=<your_project_id>
     BQ_DATASET_ID=<your_bigquery_dataset_id>
     BQ_TABLE_ID=<your_bigquery_table_id>

     # Path to your Google Cloud Service Account key file
     GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
     ```
   - Replace `<your_project_id>`, `<your_bigquery_dataset_id>`, and `<your_bigquery_table_id>` with your GCP details.
   - Provide the correct path to your **service account key JSON file**.

---

### Step 3: Set Up a Google Cloud Service Account

In order to allow Apache Airflow to interact with BigQuery, you need to set up a **service account** with the necessary permissions.

1. **Create a Service Account**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Navigate to **IAM & Admin > Service Accounts**.
   - Click **Create Service Account** and follow the prompts.
     - **Service Account Name**: `airflow-etl-service-account`
     - **Service Account ID**: Auto-generated.

2. **Grant Permissions**:
   - During service account creation, grant the following roles:
     - **BigQuery Data Editor**: Allows creating, reading, and appending BigQuery data.
     - **BigQuery Job User**: Allows the service account to submit BigQuery jobs.

3. **Download the Service Account Key**:
   - Once the service account is created, click on the service account.
   - Go to the **Keys** tab and click **Add Key > Create New Key**.
   - Choose **JSON** and download the key file.

4. **Store the Key Securely**:
   - Move the downloaded key file to your project folder (e.g., `airflow/`) or a secure location.
   - Update the `GOOGLE_APPLICATION_CREDENTIALS` path in your `.env` file to point to this key.

---

### Step 4: Run the Project Locally with Docker Compose

Once the environment is set up and the `.env` file is correctly configured, follow these steps to run Apache Airflow:

1. **Navigate to the `airflow` folder:**
   ```bash
   cd airflow
   ```

2. **Build and Run the Docker Containers:**
   ```bash
   docker-compose up --build
   ```

   This command will:
   - Initialize the Airflow database.
   - Start the Airflow web server, scheduler, PostgreSQL, and Redis.

3. **Access the Airflow UI**:
   - Open your browser and go to `http://localhost:8080`.
   - Log in with the default credentials:
     - **Username**: `airflow`
     - **Password**: `airflow`

---

### Step 5: Add Your DAG to Airflow

1. **Add your DAG file**:
   - Copy your DAG script (e.g., `coingecko_batch_dag.py`) to the `dags/` folder.
   - Airflow will automatically detect the DAG and display it in the Airflow UI.

2. **Enable the DAG**:
   - In the Airflow UI, navigate to the **DAGs** tab.
   - Find the `coingecko_etl_dag` and toggle the switch to enable it.

---

### Step 6: Trigger the ETL Pipeline

1. **Manually Trigger the DAG**:
   - In the Airflow UI, click on the `coingecko_etl_dag`.
   - Click **Trigger DAG** to run the pipeline manually.

2. **View the Task Logs**:
   - Click on individual tasks to view logs and monitor the pipeline’s progress.

---

## 🧑‍💻 How the DAG Works

The DAG performs the following steps:
1. **Create BigQuery Table**: Checks if the BigQuery table exists and creates it if necessary.
2. **Fetch Data from CoinGecko API**: Retrieves cryptocurrency data in INR from the CoinGecko API.
3. **Transform and Insert Data**: Adds metadata columns (`created_date`, `created_by`) and inserts the data into BigQuery in append mode.

---

## 🛡 Security Best Practices
- **Environment Variables**: Keep sensitive credentials like `GCP_PROJECT_ID` and `GOOGLE_APPLICATION_CREDENTIALS` in the `.env` file (which should never be committed to version control).
- **Use `env.example` for sharing setup instructions without exposing sensitive data.**

---

## 🎯 Future Enhancements
- Add more transformations to the ETL pipeline.
- Integrate monitoring and alerting for the Airflow tasks.
- Expand the pipeline to handle streaming data.

---

## 🤝 Contributing
Contributions are welcome! Please open issues or submit pull requests to suggest improvements.

---

## 📝 License
This project is licensed under the MIT License.

---

Feel free to copy and use this as your project's README! 🎯