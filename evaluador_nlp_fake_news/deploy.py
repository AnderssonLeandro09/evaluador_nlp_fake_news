import os
import subprocess
import json
from pathlib import Path

def create_requirements_file():
    """Create requirements.txt file with all dependencies"""
    requirements = [
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "pydantic>=2.5.0",
        "python-multipart>=0.0.0",
        "huggingface-hub>=0.19.4",
        "transformers>=4.36.0",
        "torch>=2.1.0",
        "pandas>=2.1.0",
        "numpy>=1.24.0",
        "numpy>=1.24.0",
        "scikit-learn>=1.3.0",
        "pytest>=7.4.3",
        "pytest-asyncio>=0.21.1",
        "httpx>=0.25.0",
        "python-dotenv>=1.0.0",
        "black>=23.11.0",
        "isort>=5.13.2",
        "mypy>=1.7.1",
    ]
    
    with open("requirements.txt", "w") as f:
        f.write("\n".join(requirements))
    
    print("[OK] Created requirements.txt")

def create_env_file():
    """Create .env file with environment variables"""
    env_content = """# Environment variables for Fake News Detection API

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
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("[OK] Created .env file")

def create_docker_compose():
    """Create docker-compose.yml for containerized deployment"""
    docker_compose = """version: '3.8'

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
"""
    
    with open("docker-compose.yml", "w") as f:
        f.write(docker_compose)
    
    print("[OK] Created docker-compose.yml")

def create_docker_file():
    """Create Dockerfile for containerized deployment"""
    dockerfile = """FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/

# Create necessary directories
RUN mkdir -p model_cache logs

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile)
    
    print("[OK] Created Dockerfile")

def create_deployment_script():
    """Create deployment script"""
    deployment_script = """#!/bin/bash

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
    f.write('\\n'.join(requirements))
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
"""
    
    with open("deploy.sh", "w") as f:
        f.write(deployment_script)
    
    # Make the script executable
    os.chmod("deploy.sh", 0o755)
    
    print("[OK] Created deploy.sh")

def create_readme():
    """Create README.md file"""
    readme = """# Fake News Detection API

This repository contains a FastAPI-based comparative evaluation platform for
Spanish fake news detection using BETO (Spanish BERT) and mBERT (Multilingual BERT) models.

## Features

- **Comparative Evaluation**: Compare performance of BETO and mBERT models on Spanish fake news detection
- **Async Processing**: Efficient async inference for improved performance
- **REST API**: Comprehensive API with endpoints for single text evaluation, batch evaluation, metrics reporting, and data export
- **SQLite Database**: Persistent storage of evaluation results
- **Comprehensive Testing**: Unit tests, integration tests, and performance tests
- **Docker Support**: Containerized deployment with Docker and docker-compose

## Architecture

The application follows a layered architecture:

1. **API Layer**: FastAPI endpoints for REST communication
2. **Business Logic Layer**: Core evaluation logic and async processing
3. **Data Access Layer**: SQLite database operations

## Installation

### Prerequisites

- Python 3.11 or higher
- pip

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/betos-mbert-fake-news-detector.git
   cd betos-mbert-fake-news-detector
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## API Endpoints

### Single Text Evaluation

**POST** `/api/v1/evaluate`

Evaluates a single text using both BETO and mBERT models.

**Request Body:**
```json
{
  "text": "This is a test text",
  "label": 1
}
```

**Response:**
```json
{
  "id": 1,
  "text": "This is a test text",
  "label": 1,
  "beto_prediction": 1,
  "mbert_prediction": 0,
  "beto_time_ms": 0.123,
  "mbert_time_ms": 0.156,
  "beto_accuracy": 1.0,
  "mbert_accuracy": 0.0,
  "beto_precision": 1.0,
  "mbert_precision": 0.0,
  "beto_recall": 1.0,
  "mbert_recall": 0.0,
  "beto_f1_score": 1.0,
  "mbert_f1_score": 0.0,
  "timestamp": "2024-01-01T12:00:00"
}
```

### Batch Evaluation

**POST** `/api/v1/dataset/evaluate`

Evaluates multiple texts using both BETO and mBERT models.

**Request Body:**
```json
{
  "texts": ["Test text 1", "Test text 2"],
  "labels": [1, 0]
}
```

**Response:**
```json
[
  {
    "id": 1,
    "text": "Test text 1",
    "label": 1,
    "beto_prediction": 1,
    "mbert_prediction": 0,
    "beto_time_ms": 0.123,
    "mbert_time_ms": 0.156,
    "beto_accuracy": 1.0,
    "mbert_accuracy": 0.0,
    "beto_precision": 1.0,
    "mbert_precision": 0.0,
    "beto_recall": 1.0,
    "mbert_recall": 0.0,
    "beto_f1_score": 1.0,
    "mbert_f1_score": 0.0,
    "timestamp": "2024-01-01T12:00:00"
}
  ],
  {
    "id": 2,
    "text": "Test text 2",
    "label": 0,
    "beto_prediction": 0,
    "mbert_prediction": 1,
    "beto_time_ms": 0.098,
    "mbert_time_ms": 0.134,
    "beto_accuracy": 1.0,
    "mbert_accuracy": 1.0,
    "beto_precision": 1.0,
    "mbert_precision": 1.0,
    "beto_recall": 1.0,
    "mbert_recall": 1.0,
    "beto_f1_score": 1.0,
    "mbert_f1_score": 1.0,
    "timestamp": "2024-01-01T12:00:01"
  }
]
```

### Metrics Report

**GET** `/api/v1/reports/metrics`

Generates comparative metrics report from all stored evaluation results.

**Response:**
```json
{
  "total_evaluations": 10,
  "beto_metrics": {
    "accuracy": 0.85,
    "precision": 0.82,
    "recall": 0.88,
    "f1_score": 0.85
 l},
  "mbert_metrics": {
    "accuracy": 0.78,
    "precision": 0.75,
    "recall": 0.81,
    "f1_score": 0.78
  },
  "comparison": {
    "beto_better": 6,
    "mbert_better": 4,
    "tie": 0
  },
  "latest_evaluation": {
    "text": "Latest test text",
    "timestamp": "2024-01-01T12:00:00",
    "beto_prediction": 1,
    "mbert_prediction": 0
  }
}
```

### Export Results

**GET** `/api/v1/results/export`

Exports all evaluation results from the database.

**Response:**
```json
[
  {
    "id": 1,
    "text": "Test text 1",
    "label": 1,
    "beto_prediction": 1,
    "mbert_prediction": 0,
    "beto_time_ms": 0.123,
    "mbert_time_ms": 0.156,
    "beto_accuracy": 1.0,
    "mbert_accuracy": 0.0,
    "beto_precision": 1.0,
    "mbert_precision": 0.0,
    "beto_recall": 1.0,
    "mbert_recall": 0.0,
    "beto_f1_score": 1.0,
    "mbert_f1_score": 0.0,
    "timestamp": "2024-01-01T12:00:00"
  }
]
```

### Health Check

**GET** `/health`

Health check endpoint to verify the API is running.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00"
}
```

## Testing

The application includes comprehensive tests:

### Unit Tests

Run unit tests:
```bash
pytest tests/ -v
```

### Integration Tests

Run integration tests:
```bash
pytest tests/ -v -k "integration"
```

### Performance Tests

Run performance tests:
```bash
pytest tests/ -v -k "performance"
```

## Deployment

### Docker Deployment

Build and run with Docker:
```bash
docker-compose up -d
```

### Local Deployment

Run locally:
```bash
python -m pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Run tests
5. Commit your changes
6. Create a pull request

## License

This project is licensed under the MIT License.
"""
    
    with open("README.md", "w") as f:
        f.write(readme)
    
    print("[OK] Created README.md")

def main():
    """Main function to create deployment files"""
    print("Creating deployment files...")
    
    create_requirements_file()
    create_env_file()
    create_docker_compose()
    create_docker_file()
    create_deployment_script()
    create_readme()
    
    print("\nDeployment setup completed successfully!")
    print("\nFiles created:")
    print("  - requirements.txt")
    print("  - .env")
    print("  - docker-compose.yml")
    print("  - Dockerfile")
    print("  - deploy.sh")
    print("  - README.md")
    
    print("\nTo deploy the application:")
    print("  1. Run the deployment script: ./deploy.sh")
    print("  2. Or manually create the files and run:")
    print("     - pip install -r requirements.txt")
    print("     - uvicorn app.main:app --host 0.0.0.0 --port 8000")

if __name__ == "__main__":
    main()
