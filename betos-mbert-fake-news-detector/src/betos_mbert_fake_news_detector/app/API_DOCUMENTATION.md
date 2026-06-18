# Fake News Detection API Documentation

## Overview

The Fake News Detection API is a FastAPI-based application that provides a comparative evaluation platform for Spanish fake news detection using BETO (Spanish BERT) and mBERT (Multilingual BERT) models.

## API Endpoints

### 1. Single Text Evaluation

**Endpoint:** `POST /api/v1/evaluate`

**Description:** Evaluates a single text using both BETO and mBERT models.

**Request Body:**
```json
{
  "text": "This is a test text",
  "label": 1
}
```

**Parameters:**
- `text` (string, required): The text to evaluate
- `label` (integer, optional): Ground truth label (1 for fake, 0 for real)

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

**Response Codes:**
- `200 OK`: Successful evaluation
- `422 Unprocessable Entity`: Invalid request body
- `500 Internal Server Error`: Server error

### 2. Batch Evaluation

**Endpoint:** `POST /api/v1/dataset/evaluate`

**Description:** Evaluates multiple texts using both BETO and mBERT models.

**Request Body:**
```json
{
  "texts": ["Test text 1", "Test text 2"],
  "labels": [1, 0]
}
```

**Parameters:**
- `texts` (array of strings, required): List of texts to evaluate
- `labels` (array of integers, optional): List of ground truth labels

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
  },
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

**Response Codes:**
- `200 OK`: Successful evaluation
- `422 Unprocessable Entity`: Invalid request body
- `500 Internal Server Error`: Server error

### 3. Metrics Report

**Endpoint:** `GET /api/v1/reports/metrics`

**Description:** Generates comparative metrics report from all stored evaluation results.

**Response:**
```json
{
  "total_evaluations": 10,
  "beto_metrics": {
    "accuracy": 0.85,
    "precision": 0.82,
    "recall": 0.88,
    "f1_score": 0.85
  },
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

**Response Codes:**
- `200 OK`: Successful metrics retrieval
- `500 Internal Server Error`: Server error

### 4. Export Results

**Endpoint:** `GET /api/v1/results/export`

**Description:** Exports all evaluation results from the database.

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

**Response Codes:**
- `200 OK`: Successful export
- `500 Internal Server Error`: Server error

### 5. Health Check

**Endpoint:** `GET /health`

**Description:** Health check endpoint to verify the API is running.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00"
}
```

**Response Codes:**
- `200 OK`: API is healthy

## Authentication

The API does not require authentication by default. All endpoints are publicly accessible.

## Error Handling

The API returns appropriate HTTP status codes for different error scenarios:

- `400 Bad Request`: Invalid request format
- `422 Unprocessable Entity`: Invalid request body (validation error)
- `500 Internal Server Error`: Server error

## Rate Limiting

The API does not implement rate limiting by default. For production use, consider implementing rate limiting.

## CORS

The API allows all origins by default. You can configure CORS in the `.env` file:

```
CORS_ORIGINS=*
```

## Database

The API uses SQLite for data storage. The database file is named `evaluation_results.db` and is stored in the application directory.

## Model Integration

The API integrates with Hugging Face Transformers to use pre-trained BETO and mBERT models. The models are loaded once at startup and cached for subsequent requests.

## Performance

The API is designed for high performance with:

- Async processing for model inference
- Batch processing for multiple texts
- Efficient database operations
- Caching of model results

## Testing

The API includes comprehensive tests:

- Unit tests for all modules
- Integration tests for API endpoints
- Performance tests
- Error handling tests

Run tests with:
```bash
pytest tests/ -v
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

## Monitoring

The API includes basic monitoring:

- Health check endpoint
- Request logging
- Error logging

For production monitoring, consider integrating with monitoring tools like Prometheus, Grafana, or ELK stack.

## Changelog

### Version 1.0.0
- Initial release
- All core features implemented
- Comprehensive testing
- Docker support

## Future Enhancements

- WebSocket support for real-time updates
- Model versioning and updates
- Advanced analytics and visualization
- Integration with external monitoring systems
- Multi-language support

## Contact

For questions, issues, or feature requests, please visit the GitHub repository.
