#!/bin/bash

# Initialize Airflow DB
airflow db init

# Create Airflow Admin User using environment variables
airflow users create \
    --username "$AIRFLOW_ADMIN_USERNAME" \
    --firstname "$AIRFLOW_ADMIN_FIRSTNAME" \
    --lastname "$AIRFLOW_ADMIN_LASTNAME" \
    --role Admin \
    --email "$AIRFLOW_ADMIN_EMAIL" \
    --password "$AIRFLOW_ADMIN_PASSWORD"

# Start Airflow Scheduler and Webserver
airflow scheduler & airflow webserver
