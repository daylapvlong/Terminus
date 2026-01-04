FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Pin versions!
RUN pip install --no-cache-dir \
    numpy==1.26.4 \
    pandas==2.1.0

COPY app/ /app/
ENV PYTHONPATH=/app