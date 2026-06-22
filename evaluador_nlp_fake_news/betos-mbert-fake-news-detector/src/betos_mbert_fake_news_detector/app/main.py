"""
Fake News Detection API with BETO and mBERT Models

This FastAPI application provides a comparative evaluation platform for
Spanish fake news detection using BETO (Spanish BERT) and mBERT (Multilingual BERT) models.

Architecture:
- API Layer: FastAPI endpoints for REST communication
- Business Logic Layer: Core evaluation logic and async processing
- Data Access Layer: SQLite database operations

Key Features:
- Async inference for improved performance
- Comparative evaluation of both models
- Persistent storage of results
- Comprehensive metrics calculation
"""

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ValidationError
from typing import List, Optional, Dict, Any
import asyncio
import time
from datetime import datetime

from .services.service import get_evaluation_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Fake News Detection API",
    description="Comparative evaluation platform for BETO and mBERT models on Spanish fake news detection",
    version="1.0.0"
)

# Allow CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the evaluation service instance
service = get_evaluation_service()

# Pydantic models for request/response validation
class TextEvaluationRequest(BaseModel):
    text: str
    label: Optional[int] = None  # 1 for fake, 0 for real

class BatchEvaluationRequest(BaseModel):
    texts: List[str]
    labels: Optional[List[int]] = None

class EvaluationResult(BaseModel):
    id: int
    text: str
    label: Optional[int]
    beto_prediction: int
    mbert_prediction: int
    beto_time_ms: float
    mbert_time_ms: float
    beto_accuracy: float
    mbert_accuracy: float
    beto_precision: float
    mbert_precision: float
    beto_recall: float
    mbert_recall: float
    beto_f1_score: float
    mbert_f1_score: float
    timestamp: str

# API Endpoints
@app.post("/api/v1/evaluate", response_model=EvaluationResult)
async def evaluate_single_text(request: TextEvaluationRequest):
    """
    Evaluate a single text using both BETO and mBERT models.
    
    Args:
        request: Text and optional ground truth label
        
    Returns:
        EvaluationResult containing predictions and metrics from both models
    """
    try:
        logger.info(f"Evaluating text: {request.text[:50]}...")
        result = await service.evaluate_text(request.text, request.label)
        logger.info(f"Evaluation completed successfully. Result ID: {result.id}")
        return result
    except ValidationError as e:
        logger.error(f"Validation error in evaluate_single_text: {e}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Error in evaluate_single_text: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/api/v1/dataset/evaluate", response_model=List[EvaluationResult])
async def evaluate_batch_texts(request: BatchEvaluationRequest):
    """
    Evaluate multiple texts using both BETO and mBERT models.
    
    Args:
        request: List of texts and optional ground truth labels
        
    Returns:
        List of EvaluationResult objects for each text
    """
    try:
        logger.info(f"Evaluating batch of {len(request.texts)} texts")
        results = await service.evaluate_batch(request.texts, request.labels)
        logger.info(f"Batch evaluation completed successfully. Processed {len(results)} texts")
        return results
    except ValidationError as e:
        logger.error(f"Validation error in evaluate_batch_texts: {e}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Error in evaluate_batch_texts: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/v1/reports/metrics", response_model=Dict[str, Any])
async def get_comparative_metrics():
    """
    Generate comparative metrics report from all stored evaluation results.
    
    Returns:
        Dictionary containing aggregated metrics for both models
    """
    try:
        logger.info("Generating comparative metrics report")
        metrics = service.get_comparative_metrics()
        logger.info(f"Comparative metrics report generated. Total evaluations: {metrics['total_evaluations']}")
        return metrics
    except Exception as e:
        logger.error(f"Error in get_comparative_metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/v1/results/export", response_model=List[EvaluationResult])
async def export_results():
    """
    Export all evaluation results from the database.
    
    Returns:
        List of all EvaluationResult objects
    """
    try:
        logger.info("Exporting evaluation results")
        results = service.export_results()
        logger.info(f"Exported {len(results)} evaluation results")
        return results
    except Exception as e:
        logger.error(f"Error in export_results: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint to verify the API is running."""
    logger.info("Health check requested")
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
