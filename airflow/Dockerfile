# Use the official Apache Airflow image
FROM apache/airflow:2.5.3

# Set environment variables (optional, safe defaults)
ENV AIRFLOW_HOME=/opt/airflow

# Switch to root to install packages
USER root

# Install Google Cloud SDK and dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    python3-dev \
    gcc \
    && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - \
    && echo "deb https://packages.cloud.google.com/apt cloud-sdk main" \
    | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
    && apt-get update && apt-get install -y google-cloud-sdk \
    && apt-get clean

# Switch back to airflow user
USER airflow

# Copy the DAGs, plugins, and requirements
COPY dags/ /opt/airflow/dags/
COPY plugins/ /opt/airflow/plugins/
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
