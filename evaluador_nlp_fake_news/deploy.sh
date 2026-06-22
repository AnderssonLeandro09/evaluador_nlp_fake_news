#!/bin/bash

# Deployment script for Fake News Detection API

set -e

echo "Starting deployment..."

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "Creating requirements.txt..."
    python -c "
import json
import os

# Read existing requirements
requirements = [
    'fastapi>=0.104.1',
    'uvicorn>=0.24.0',
    'pydantic>=2.5.0',
    'python-multipart>=0.0.0',
    'huggingface-hub>=0.19.4',
    'transformers>=4.36.0',
    'torch>=2.1.0',
    'sqlite3>=2.5.0',
    'pandas>=2.1.0',
    'numpy>=1.24.0',
    'scikit-learn>=1.3.0',
    'pytest>=7.4.3',
    'pytest-asyncio>=0.21.1',
    'httpx>=0.25.0',
    'python-dotenv>=1.0.0',
    'black>=23.11.0',
    'isort>=5.13.2',
    'mypy>=1.7.1',
]

with open('requirements.txt', 'w') as f:
    f.write('\n'.join(requirements))
"
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOF
# Environment variables for Fake News Detection API

# API configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# Database configuration
DATABASE_PATH=evaluation_results.db

# Model configuration
MODEL_CACHE_DIR=./model_cache
MAX_TEXT_LENGTH=512
BATCH_SIZE=32

# Logging configuration
LOG_LEVEL=INFO
LOG_FILE=app.log

# CORS configuration
CORS_ORIGINS=*

# Security configuration
SECRET_KEY=your-secret-key-here
EOF
fi

# Check if docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
    echo "Creating docker-compose.yml..."
    cat > docker-compose.yml << EOF
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///evaluation_results.db
      - PYTHONPATH=/app/src
    volumes:
      - ./:/app
      - ./model_cache:/root/.cache/huggingface
    restart: unless-stopped
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000

  worker:
    build: .
    environment:
      - PYTHONPATH=/app/src
    volumes:
      - ./:/app
      - ./model_cache:/root/.cache/huggingface
    command: python -m pytest tests/ -v
    depends_on:
      - app
EOF
fi

# Check if Dockerfile exists
if [ ! -f "Dockerfile" ]; then
    echo "Creating Dockerfile..."
    cat > Dockerfile << EOF
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

RUN mkdir -p model_cache logs

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF
fi

echo "Deployment setup completed successfully!"
echo "You can now deploy the application using:")
echo "  - Docker: docker-compose up -d"
echo "  - Local: python -m pip install -r requirements.txt && uvicorn app.main:app --host 0.0.0.0 --port 8000"
