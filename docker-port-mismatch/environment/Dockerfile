FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies with pinned versions
RUN pip install --no-cache-dir \
    flask==3.0.0 \
    werkzeug==3.0.1

# Copy application code
COPY app/ /app/

# BUG: Wrong port - app listens on 5000 but Dockerfile exposes 8080
EXPOSE 8080

# Start the server
CMD ["python", "server.py"]