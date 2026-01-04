FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY app/ /app/

# Create directories (data will be mounted by test.sh)
RUN mkdir -p /data /output

# Set Python path
ENV PYTHONPATH=/app