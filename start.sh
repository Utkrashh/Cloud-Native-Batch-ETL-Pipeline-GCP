#!/bin/bash

# Wait for Airflow to initialize the database (just in case)
echo "Waiting for Airflow to initialize..."
sleep 30

# Create the Airflow admin user if it doesn't already exist
echo "Creating Airflow admin user..."

airflow users create \
  --username ${AIRFLOW_ADMIN_USERNAME} \
  --firstname ${AIRFLOW_ADMIN_FIRSTNAME} \
  --lastname ${AIRFLOW_ADMIN_LASTNAME} \
  --role Admin \
  --email ${AIRFLOW_ADMIN_EMAIL} \
  --password ${AIRFLOW_ADMIN_PASSWORD}

# Start Airflow webserver and scheduler
echo "Starting Airflow webserver and scheduler..."
airflow webserver & airflow scheduler
