# Use official Airflow image as the base
FROM apache/airflow:2.5.3

# Switch to root to install system dependencies
USER root

# Install system dependencies (e.g., gcc, libpq-dev for PostgreSQL support)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean

# Switch back to airflow user
USER airflow

# Set working directory
WORKDIR /opt/airflow

# Copy requirements first for layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into image
COPY airflow/dags /opt/airflow/dags
COPY start.sh /start.sh

# Make the startup script executable
RUN chmod +x /start.sh

# Set environment variables for Airflow
ENV AIRFLOW__CORE__EXECUTOR=LocalExecutor
ENV AIRFLOW__CORE__FERNET_KEY=${FERNET_KEY}
ENV AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}

# Expose Airflow webserver port
EXPOSE 8080

# Set the default command (calls start.sh which handles everything)
CMD ["bash", "-c", "/start.sh && airflow webserver && airflow scheduler"]