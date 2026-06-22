from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..schemas.schemas import TextEvaluationRequest, BatchEvaluationRequest, EvaluationResponse
from ..services.evaluator import evaluation_service
from ..db.database import db_session
from datetime import datetime

router = APIRouter()

@router.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_text(request: TextEvaluationRequest):
    """Evalúa un texto utilizando BETO y mBERT de forma asíncrona."""
    try:
        beto_res, mbert_res = await evaluation_service.evaluate(request.text, request.label)
        
        # Persistencia en SQLite
        with db_session() as conn:
            cursor = conn.execute(
                "INSERT INTO evaluation_results (text, label, beto_prediction, mbert_prediction, beto_time_ms, mbert_time_ms, beto_accuracy, mbert_accuracy, beto_precision, mbert_precision, beto_recall, mbert_recall, beto_f1_score, mbert_f1_score, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (request.text, request.label, beto_res.prediction, mbert_res.prediction, beto_res.time_ms, mbert_res.time_ms, beto_res.accuracy, mbert_res.accuracy, 0.0, 0.0, 0.0, 0.0, beto_res.f1_score, mbert_res.f1_score, datetime.now().isoformat())
            )
            result_id = cursor.lastrowid
            conn.commit()

        return EvaluationResponse(
            id=result_id,
            text=request.text,
            label=request.label,
            beto_result=beto_res,
            mbert_result=mbert_res,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch-evaluate", response_model=List[EvaluationResponse])
async def evaluate_batch(request: BatchEvaluationRequest):
    """Evalúa un lote de textos."""
    results = []
    for text in request.texts:
        # Reusamos la lógica de evaluación simple para el MVP
        res = await evaluate_text(TextEvaluationRequest(text=text, label=None))
        results.append(res)
    return results
