from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class TextEvaluationRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Texto de la noticia a evaluar")
    label: Optional[int] = Field(None, ge=0, le=1, description="Etiqueta real: 1=Fake, 0=Real")

class BatchEvaluationRequest(BaseModel):
    texts: List[str] = Field(..., min_items=1)
    labels: Optional[List[int]] = None

class ModelPrediction(BaseModel):
    model_name: str
    prediction: int
    time_ms: float
    accuracy: float
    f1_score: float

class EvaluationResponse(BaseModel):
    id: Optional[int] = None
    text: str
    label: Optional[int]
    beto_result: ModelPrediction
    mbert_result: ModelPrediction
    timestamp: datetime = Field(default_factory=datetime.now)
