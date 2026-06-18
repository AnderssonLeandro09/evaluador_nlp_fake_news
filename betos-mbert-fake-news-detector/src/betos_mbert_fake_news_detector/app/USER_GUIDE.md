# Fake News Detection API - User Guide

## Welcome to the Fake News Detection API!

This guide will help you get started with the Fake News Detection API and make the most of its features.

## Quick Start

### Prerequisites

- Python 3.11 or higher
- pip
- Basic understanding of REST APIs

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/betos-mbert-fake-news-detector.git
   cd betos-mbert-fake-news-detector
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## API Endpoints

### 1. Single Text Evaluation

**Purpose:** Evaluate a single text using both BETO and mBERT models.

**Example Request:**
```bash
curl -X POST http://localhost:8000/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a test text about fake news", "label": 1}'
```

**Example Response:**
```json
{
  "id": 1,
  "text": "This is a test text about fake news",
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

### 2. Batch Evaluation

**Purpose:** Evaluate multiple texts using both BETO and mBERT models.

**Example Request:**
```bash
curl -X POST http://localhost:8000/api/v1/dataset/evaluate \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Fake news example 1", "Real news example 2"], "labels": [1, 0]}'
```

**Example Response:**
```json
[
  {
    "id": 1,
    "text": "Fake news example 1",
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
    "text": "Real news example 2",
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

### 3. Metrics Report

**Purpose:** Get comparative metrics report from all stored evaluation results.

**Example Request:**
```bash
curl -X GET http://localhost:8000/api/v1/reports/metrics
```

**Example Response:**
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

### 4. Export Results

**Purpose:** Export all evaluation results from the database.

**Example Request:**
```bash
curl -X GET http://localhost:8000/api/v1/results/export
```

**Example Response:**
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

### 5. Health Check

**Purpose:** Check if the API is running.

**Example Request:**
```bash
curl -X GET http://localhost:8000/health
```

**Example Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00"
}
```

## Using the API Programmatically

### Python Example

```python
import requests
import json

# Base URL
base_url = "http://localhost:8000/api/v1"

# Single text evaluation
response = requests.post(
    f"{base_url}/evaluate",
    json={
        "text": "This is a test text about fake news",
        "label": 1
    }
)

if response.status_code == 200:
    result = response.json()
    print(f"Evaluation ID: {result['id']}")
    print(f"BETO Prediction: {result['beto_prediction']}")
    print(f"mBERT Prediction: {result['mbert_prediction']}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)

# Batch evaluation
response = requests.post(
    f"{base_url}/dataset/evaluate",
    json={
        "texts": ["Fake news example 1", "Real news example 2"],
        "labels": [1, 0]
    }
)

if response.status_code == 200:
    results = response.json()
    for result in results:
        print(f"Text: {result['text']}")
        print(f"BETO Prediction: {result['beto_prediction']}")
        print(f"mBERT Prediction: {result['mbert_prediction']}")
        print("---")
else:
    print(f"Error: {response.status_code}")
    print(response.text)

# Get metrics
response = requests.get(f"{base_url}/reports/metrics")

if response.status_code == 200:
    metrics = response.json()
    print(f"Total Evaluations: {metrics['total_evaluations']}")
    print(f"BETO Accuracy: {metrics['beto_metrics']['accuracy']}")
    print(f"mBERT Accuracy: {metrics['mbert_metrics']['accuracy']}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
```

### JavaScript Example (Node.js with axios)

```javascript
const axios = require('axios');

const baseURL = 'http://localhost:8000/api/v1';

// Single text evaluation
axios.post(`${baseURL}/evaluate`, {
    text: 'This is a test text about fake news',
    label: 1
})
.then(response => {
    const result = response.data;
    console.log(`Evaluation ID: ${result.id}`);
    console.log(`BETO Prediction: ${result.beto_prediction}`);
    console.log(`mBERT Prediction: ${result.mbert_prediction}`);
})
.catch(error => {
    console.error('Error:', error.response?.status, error.response?.data);
});

// Batch evaluation
axios.post(`${baseURL}/dataset/evaluate`, {
    texts: ['Fake news example 1', 'Real news example 2'],
    labels: [1, 0]
})
.then(response => {
    const results = response.data;
    results.forEach(result => {
        console.log(`Text: ${result.text}`);
        console.log(`BETO Prediction: ${result.beto_prediction}`);
        console.log(`mBERT Prediction: ${result.mbert_prediction}`);
        console.log('---');
    });
})
.catch(error => {
    console.error('Error:', error.response?.status, error.response?.data);
});

// Get metrics
axios.get(`${baseURL}/reports/metrics`)
.then(response => {
    const metrics = response.data;
    console.log(`Total Evaluations: ${metrics.total_evaluations}`);
    console.log(`BETO Accuracy: ${metrics.beto_metrics.accuracy}`);
    console.log(`mBERT Accuracy: ${metrics.mbert_metrics.accuracy}`);
})
.catch(error => {
    console.error('Error:', error.response?.status, error.response?.data);
});
```

## Data Formats

### Request Formats

All API endpoints accept JSON data. The request body should be formatted as follows:

#### Single Text Evaluation
```json
{
  "text": "string (required)",
  "label": "integer (optional)"
}
```

#### Batch Evaluation
```json
{
  "texts": ["string", "string"],
  "labels": [1, 0]
}
```

### Response Formats

All successful responses return JSON data. The response format varies depending on the endpoint:

#### Single Text Evaluation
```json
{
  "id": "integer",
  "text": "string",
  "label": "integer or null",
  "beto_prediction": "integer",
  "mbert_prediction": "integer",
  "beto_time_ms": "float",
  "mbert_time_ms": "float",
  "beto_accuracy": "float",
  "mbert_accuracy": "float",
  "beto_precision": "float",
  "mbert_precision": "float",
  "beto_recall": "float",
  "mbert_recall": "float",
  "beto_f1_score": "float",
  "mbert_f1_score": "float",
  "timestamp": "string"
}
```

#### Batch Evaluation
```json
[
  {
    "id": "integer",
    "text": "string",
    "label": "integer or null",
    "beto_prediction": "integer",
    "mbert_prediction": "integer",
    "beto_time_ms": "float",
    "mbert_time_ms": "float",
    "beto_accuracy": "float",
    "mbert_accuracy": "float",
    "beto_precision": "float",
    "mbert_precision": "float",
    "beto_recall": "float",
    "mbert_recall": "float",
    "beto_f1_score": "float",
    "mbert_f1_score": "float",
    "timestamp": "string"
  }
]
```

#### Metrics Report
```json
{
  "total_evaluations": "integer",
  "beto_metrics": {
    "accuracy": "float",
    "precision": "float",
    "recall": "float",
    "f1_score": "float"
  },
  "mbert_metrics": {
    "accuracy": "float",
    "precision": "float",
    "recall": "float",
    "f1_score": "float"
  },
  "comparison": {
    "beto_better": "integer",
    "mbert_better": "integer",
    "tie": "integer"
  },
  "latest_evaluation": {
    "text": "string",
    "timestamp": "string",
    "beto_prediction": "integer",
    "mbert_prediction": "integer"
  }
}
```

#### Export Results
```json
[
  {
    "id": "integer",
    "text": "string",
    "label": "integer or null",
    "beto_prediction": "integer",
    "mbert_prediction": "integer",
    "beto_time_ms": "float",
    "mbert_time_ms": "float",
    "beto_accuracy": "float",
    "mbert_accuracy": "float",
    "beto_precision": "float",
    "mbert_precision": "float",
    "beto_recall": "float",
    "mbert_recall": "float",
    "beto_f1_score": "float",
    "mbert_f1_score": "float",
    "timestamp": "string"
  }
]
```

## Error Handling

The API returns appropriate HTTP status codes for different error scenarios:

### 400 Bad Request
Returned when the request body is malformed or missing required fields.

### 422 Unprocessable Entity
Returned when the request body is valid but contains invalid data.

### 500 Internal Server Error
Returned when an unexpected error occurs on the server.

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

## Frequently Asked Questions

### Q: How do I handle API errors?

A: The API returns appropriate HTTP status codes for different error scenarios. Check the status code and response body for error details.

### Q: Can I use this API from a web application?

A: Yes, the API supports CORS by default. You can make requests from web applications running in browsers.

### Q: How do I get started with the API?

A: Follow the "Quick Start" section in this guide. It provides step-by-step instructions for setting up the API and making your first requests.

### Q: What are the performance characteristics?

 A: The API is designed for high performance with async processing and batch operations. Performance can vary based on the size of the input data and available system resources.

### Q: How do I deploy this API in production?

A: The API supports Docker deployment. Refer to the "Deployment" section for detailed instructions on deploying with Docker.

## Troubleshooting

### Common Issues

1. **Connection Refused**: Ensure the API is running and listening on the specified port.

2. **Invalid JSON**: Ensure the request body is valid JSON.

3. **Missing Fields**: Ensure all required fields are present in the request body.

4. **Large Requests**: For large batch evaluations, ensure the request size is within acceptable limits.

### Getting Help

If you encounter issues, please:

1. Check the API logs for error details
2. Verify the request format
3. Check the API health endpoint
4. Consult the documentation
5. If the issue persists, please report it on the GitHub repository

## Conclusion

The Fake News Detection API provides a comprehensive platform for comparing BETO and mBERT models on Spanish fake news detection. With its REST API, comprehensive testing, and Docker support, it's ready for production use.

Start building your fake news detection applications today!
