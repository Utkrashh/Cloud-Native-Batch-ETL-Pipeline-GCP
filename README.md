# Cloud-Native ETL Pipeline: Batch & Streaming Data Processing

This project demonstrates a **Cloud-Native ETL Pipeline** using **Apache Airflow**, **Google Cloud Platform (GCP)** services, and **Docker** to handle both **batch** and **real-time (streaming)** data processing.

## **Overview**

The pipeline automates the extraction, transformation, and loading (ETL) of data, leveraging the following technologies:
- **Batch Data Processing**: Scheduled ETL jobs using **Apache Airflow** (managed by **Cloud Composer**) to process large datasets.
- **Streaming Data Processing**: Real-time ETL pipeline triggered by **GCP Pub/Sub** events.
- **Dockerized Setup**: Local development with Docker containers for easy replication of the cloud setup.

## **Features**
- **Batch ETL Pipeline**: Processes and transforms large datasets stored in **Google Cloud Storage** and loads them into **BigQuery**.
- **Streaming ETL Pipeline**: Ingests real-time data from **GCP Pub/Sub**, applies transformations, and stores the results in BigQuery.
- **CI/CD Integration**: Automated deployment of Airflow DAGs using **GitHub Actions**.
- **Cloud-Native Design**: Scalable and cost-effective, leveraging managed services like **Cloud Composer** and **BigQuery**.

---

## **Technologies Used**
- **Apache Airflow** (Orchestrates the ETL pipeline)
- **Google Cloud Platform (GCP)**:
  - **Cloud Composer**: Managed Apache Airflow service
  - **Cloud Storage**: Stores input/output datasets
  - **BigQuery**: Data warehouse for analytics and querying
  - **Pub/Sub**: Message broker for real-time data ingestion
- **Docker & Docker Compose** (Local Airflow setup)
- **GitHub Actions** (CI/CD for DAG deployment)

---

## **Project Architecture**
The project consists of the following key components:

1. **Batch ETL Workflow**  
   - Scheduled daily to extract, transform, and load batch datasets.
   - Executes Airflow DAG that:
     - Extracts data from Google Cloud Storage
     - Transforms it using Python and Pandas
     - Loads it into BigQuery for analytics and reporting

2. **Streaming ETL Workflow**  
   - Triggered automatically when new data arrives in GCS (via Pub/Sub event notifications).
   - Processes streaming data in real time.

3. **CI/CD Workflow**  
   - Automates deployment of Airflow DAGs to Cloud Composer whenever code is pushed to the GitHub repository.

---

## **Setup Instructions**

### **1. Prerequisites**
Before you begin, ensure you have the following:
- A **Google Cloud Platform (GCP)** account
- **Docker** and **Docker Compose** installed
- **Python 3.8+** installed locally
- **GitHub repository** setup (you can fork this project)

### **2. Clone the Repository**
```bash
git clone https://github.com/utkrashh/Cloud-Native-ETL-Pipeline-Batch-Streaming-Data-Processing.git
cd Cloud-Native-ETL-Pipeline-Batch-Streaming-Data-Processing
