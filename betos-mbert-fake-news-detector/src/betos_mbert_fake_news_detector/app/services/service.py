"""
Service layer for Fake News Detection API

This module contains the business logic and core functionality
for the BETO and mBERT model comparison platform.
"""

import asyncio
import time
from datetime import datetime
from typing import List, Optional, Dict, Any
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass

from fastapi import HTTPException

# Database setup
@contextmanager
def get_db_connection():
    """Context manager for SQLite database connections"""
    conn = sqlite3.connect("evaluation_results.db")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# Data models
@dataclass
class EvaluationResult:
    """Data class for evaluation results"""
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

@dataclass
class ModelMetrics:
    """Data class for model metrics"""
    accuracy: float
    precision: float
    recall: float
    f1_score: float

class EvaluationService:
    """Service class for evaluation business logic"""
    
    def __init__(self):
        self.db_initialized = False
    
    def initialize_database(self):
        """Initialize the database table if it doesn't exist"""
        with get_db_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS evaluation_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    label INTEGER,
                    beto_prediction INTEGER NOT NULL,
                    mbert_prediction INTEGER NOT NULL,
                    beto_time_ms REAL NOT NULL,
                    mbert_time_ms REAL NOT NULL,
                    beto_accuracy REAL NOT NULL,
                    mbert_accuracy REAL NOT NULL,
                    beto_precision REAL NOT NULL,
                    mbert_precision REAL NOT NULL,
                    beto_recall REAL NOT NULL,
                    mbert_recall REAL NOT NULL,
                    beto_f1_score REAL NOT NULL,
                    mbert_f1_score REAL NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)
            conn.commit()
        self.db_initialized = True
    
    async def mock_beto_inference(self, text: str) -> tuple[int, float]:
        """Mock BETO model inference - simulate processing time"""
        await asyncio.sleep(0.1)
        prediction = len(text) % 2
        processing_time = 0.1 + (len(text) * 0.001)
        return prediction, processing_time
    
    async def mock_mbert_inference(self, text: str) -> tuple[int, float]:
        """Mock mBERT model inference - simulate processing time"""
        await asyncio.sleep(0.15)
        prediction = len(text) % 3
        processing_time = 0.15 + (len(text) * 0.0015)
        return prediction, processing_time
    
    def calculate_metrics(self, predictions: List[int], labels: List[int]) -> ModelMetrics:
        """Calculate accuracy, precision, recall, and F1-score"""
        if not labels or len(predictions) != len(labels):
            return ModelMetrics(0.0, 0.0, 0.0, 0.0)
        
        true_positives = sum(1 for p, l in zip(predictions, labels) if p == 1 and l == 1)
        true_negatives = sum(1 for p, l in zip(predictions, labels) if p == 0 and l == 0)
        false_positives = sum(1 for p, l in zip(predictions, labels) if p == 1 and l == 0)
        false_negatives = sum(1 for p, l in zip(predictions, labels) if p == 0 and l == 1)
        
        total = len(predictions)
        accuracy = (true_positives + true_negatives) / total if total > 0 else 0.0
        
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
        
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        
        return ModelMetrics(accuracy, precision, recall, f1_score)
    
    async def evaluate_text(self, text: str, label: Optional[int] = None) -> EvaluationResult:
        """
        Evaluate a single text using both models.
        
        Args:
            text: Input text to evaluate
            label: Optional ground truth label
            
        Returns:
            EvaluationResult object
        """
        # Perform async inference for both models concurrently
        beto_task = self.mock_beto_inference(text)
        mbert_task = self.mock_mbert_inference(text)
        
        beto_prediction, beto_time = await beto_task
        mbert_prediction, mbert_time = await mbert_task
        
        # Calculate metrics
        labels = [label] if label is not None else []
        
        beto_metrics = self.calculate_metrics([beto_prediction], labels)
        mbert_metrics = self.calculate_metrics([mbert_prediction], labels)
        
        # Store results in database
        with get_db_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO evaluation_results 
                (text, label, beto_prediction, mbert_prediction, 
                 beto_time_ms, mbert_time_ms, beto_accuracy, mbert_accuracy,
                 beto_precision, mbert_precision, beto_recall, mbert_recall,
                 beto_f1_score, mbert_f1_score, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    text,
                    label,
                    beto_prediction,
                    mbert_prediction,
                    beto_time,
                    mbert_time,
                    beto_metrics.accuracy,
                    mbert_metrics.accuracy,
                    beto_metrics.precision,
                    mbert_metrics.precision,
                    beto_metrics.recall,
                    mbert_metrics.recall,
                    beto_metrics.f1_score,
                    mbert_metrics.f1_score,
                    datetime.now().isoformat()
                )
            )
            result_id = cursor.lastrowid
            conn.commit()
        
        # Return the evaluation result
        return EvaluationResult(
            id=result_id,
            text=text,
            label=label,
            beto_prediction=beto_prediction,
            mbert_prediction=mbert_prediction,
            beto_time_ms=beto_time,
            mbert_time_ms=mbert_time,
            beto_accuracy=beto_metrics.accuracy,
            mbert_accuracy=mbert_metrics.accuracy,
            beto_precision=beto_metrics.precision,
            mbert_precision=mbert_metrics.precision,
            beto_recall=beto_metrics.recall,
            mbert_recall=mbert_metrics.recall,
            beto_f1_score=beto_metrics.f1_score,
            mbert_f1_score=mbert_metrics.f1_score,
            timestamp=datetime.now().isoformat()
        )
    
    async def evaluate_batch(self, texts: List[str], labels: Optional[List[int]] = None) -> List[EvaluationResult]:
        """
        Evaluate multiple texts using both models.
        
        Args:
            texts: List of input texts to evaluate
            labels: Optional list of ground truth labels
            
        Returns:
            List of EvaluationResult objects
        """
        results = []
        
        for i, text in enumerate(texts):
            label = labels[i] if labels and i < len(labels) else None
            result = await self.evaluate_text(text, label)
            results.append(result)
        
        return results
    
    def get_comparative_metrics(self) -> Dict[str, Any]:
        """
        Generate comparative metrics report from all stored evaluation results.
        
        Returns:
            Dictionary containing aggregated metrics for both models
        """
        with get_db_connection() as conn:
            cursor = conn.execute("SELECT * FROM evaluation_results ORDER BY timestamp DESC")
            rows = cursor.fetchall()
            
            if not rows:
                return {
                    "total_evaluations": 0,
                    "beto_metrics": {"accuracy": 0.0, "precision": 0.0, "recall": 0.0, "f1_score": 0.0},
                    "mbert_metrics": {"accuracy": 0.0, "precision": 0.0, "recall": 0.0, "f1_score": 0.0},
                    "comparison": {"beto_better": 0, "mbert_better": 0, "tie": 0}
                }
            
            # Calculate aggregated metrics
            beto_accuracies = [row["beto_accuracy"] for row in rows]
            mbert_accuracies = [row["mbert_accuracy"] for row in rows]
            
            beto_precisions = [row["beto_precision"] for row in rows]
            mbert_precisions = [row["mbert_precision"] for row in rows]
            
            beto_recalls = [row["beto_recall"] for row in rows]
            mbert_recalls = [row["mbert_recall"] for row in rows]
            
            beto_f1_scores = [row["beto_f1_score"] for row in rows]
            mbert_f1_scores = [row["mbert_f1_score"] for row in rows]
            
            def average(values):
                return sum(values) / len(values) if values else 0.0
            
            # Compare model performance
            beto_better = sum(1 for b, m in zip(beto_accuracies, mbert_accuracies) if b > m)
            mbert_better = sum(1 for b, m in zip(beto_accuracies, mbert_accuracies) if m > b)
            tie = sum(1 for b, m in zip(beto_accuracies, mbert_accuracies) if b == m)
            
            return {
                "total_evaluations": len(rows),
                "beto_metrics": {
                    "accuracy": average(beto_accuracies),
                    "precision": average(beto_precisions),
                    "recall": average(beto_recalls),
                    "f1_score": average(beto_f1_scores)
                },
                "mbert_metrics": {
                    "accuracy": average(mbert_accuracies),
                    "precision": average(mbert_precisions),
                    "recall": average(mbert_recalls),
                    "f1_score": average(mbert_f1_scores)
                },
                "comparison": {
                    "beto_better": beto_better,
                    "mbert_better": mbert_better,
                    "tie": tie
                },
                "latest_evaluation": {
                    "text": rows[0]["text"],
                    "timestamp": rows[0]["timestamp"],
                    "beto_prediction": rows[0]["beto_prediction"],
                    "mbert_prediction": rows[0]["mbert_prediction"]
                }
            }
    
    def export_results(self) -> List[EvaluationResult]:
        """
        Export all evaluation results from the database.
        
        Returns:
            List of all EvaluationResult objects
        """
        with get_db_connection() as conn:
            cursor = conn.execute("SELECT * FROM evaluation_results ORDER BY timestamp DESC")
            rows = cursor.fetchall()
            
            results = []
            for row in rows:
                result = EvaluationResult(
                    id=row["id"],
                    text=row["text"],
                    label=row["label"],
                    beto_prediction=row["beto_prediction"],
                    mbert_prediction=row["mbert_prediction"],
                    beto_time_ms=row["beto_time_ms"],
                    mbert_time_ms=row["mbert_time_ms"],
                    beto_accuracy=row["beto_accuracy"],
                    mbert_accuracy=row["mbert_accuracy"],
                    beto_precision=row["beto_precision"],
                    mbert_precision=row["mbert_precision"],
                    beto_recall=row["beto_recall"],
                    mbert_recall=row["mbert_recall"],
                    beto_f1_score=row["beto_f1_score"],
                    mbert_f1_score=row["mbert_f1_score"],
                    timestamp=row["timestamp"]
                )
                results.append(result)
            
            return results

# Create a singleton instance of the service
_evaluation_service = None

def get_evaluation_service() -> EvaluationService:
    """Get the singleton evaluation service instance"""
    global _evaluation_service
    if _evaluation_service is None:
        _evaluation_service = EvaluationService()
        _evaluation_service.initialize_database()
    return _evaluation_service
