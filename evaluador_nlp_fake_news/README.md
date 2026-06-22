# Fake News Detection API

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
