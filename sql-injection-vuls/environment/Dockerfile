FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY app/ /app/

# Create data directory
RUN mkdir -p /data /output

# Set Python path
ENV PYTHONPATH=/app