#!/bin/bash

# Wait for Airflow to initialize the database (just in case)
echo "Waiting for Airflow to initialize..."
sleep 30

# Create the Airflow admin user if it doesn't already exist
echo "Creating Airflow admin user..."

airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password admin

# Start Airflow webserver and scheduler
echo "Starting Airflow webserver and scheduler..."
airflow webserver & airflow scheduler
