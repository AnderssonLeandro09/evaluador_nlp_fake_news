import asyncio
import time
import torch
from typing import List, Optional, Tuple, Dict
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from ..schemas.schemas import ModelPrediction

class EvaluationService:
    """
    Servicio encargado de la lógica de inferencia real utilizando
    modelos BETO y mBERT mediante Hugging Face Transformers.
    """
    
    def __init__(self):
        # Modelos y Tokenizadores
        self.beto_name = "dccuchile/bert-base-spanish-wwm-uncased"
        self.mbert_name = "bert-base-multilingual-cased"
        
        self.beto_tokenizer = None
        self.beto_model = None
        self.mbert_tokenizer = None
        self.mbert_model = None
        
        self.models_loaded = False

    async def load_models(self):
        """
        Carga los modelos y tokenizadores en memoria.
        Se utiliza asyncio.to_thread ya que la carga de modelos es una operación bloqueante de I/O y CPU.
        """
        def _load():
            # Carga BETO
            self.beto_tokenizer = AutoTokenizer.from_pretrained(self.beto_name)
            self.beto_model = AutoModelForSequenceClassification.from_pretrained(self.beto_name)
            
            # Carga mBERT
            self.mbert_tokenizer = AutoTokenizer.from_pretrained(self.mbert_name)
            self.mbert_model = AutoModelForSequenceClassification.from_pretrained(self.mbert_name)
            
        await asyncio.to_thread(_load)
        self.models_loaded = True

    def _predict_sync(self, text: str, tokenizer, model) -> Tuple[int, float]:
        """
        Sincroniza la inferencia de PyTorch.
        Retorna la predicción (clase) y el tiempo de ejecución en ms.
        """
        start_time = time.perf_counter()
        
        # Tokenización y preparación de tensores
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        
        # Inferencia (sin gradientes para optimizar)
        with torch.no_grad():
            outputs = model(**inputs)
            # Obtenemos el índice del valor más alto (predicción de clase)
            prediction = torch.argmax(outputs.logits, dim=-1).item()
            
        end_time = time.perf_counter()
        processing_time = (end_time - start_time) * 1000
        
        return int(prediction), processing_time

    async def _infer_beto(self, text: str) -> Tuple[int, float]:
        """Ejecuta la inferencia de BETO en un hilo separado para evitar bloquear FastAPI."""
        return await asyncio.to_thread(self._predict_sync, text, self.beto_tokenizer, self.beto_model)

    async def _infer_mbert(self, text: str) -> Tuple[int, float]:
        """Ejecuta la inferencia de mBERT en un hilo separado para evitar bloquear FastAPI."""
        return await asyncio.to_thread(self._predict_sync, text, self.mbert_tokenizer, self.mbert_model)

    async def evaluate(self, text: str, label: Optional[int] = None) -> Tuple[ModelPrediction, ModelPrediction]:
        """
        Orquestador de inferencia paralela.
        Ejecuta BETO y mBERT concurrentemente y calcula métricas básicas.
        """
        if not self.models_loaded:
            await self.load_models()

        # Ejecución paralela de inferencias
        beto_res, mbert_res = await asyncio.gather(
            self._infer_beto(text),
            self._infer_mbert(text)
        )

        # Cálculo de métricas básicas para una sola instancia
        # Si hay etiqueta, Accuracy es 1.0 si coincide, 0.0 si no.
        def get_metrics(pred, label):
            if label is None:
                return 0.0, 0.0
            acc = 1.0 if pred == label else 0.0
            return acc, acc # Para una sola muestra, acc=prec=rec=f1

        beto_acc, beto_f1 = get_metrics(beto_res[0], label)
        mbert_acc, mbert_f1 = get_metrics(mbert_res[0], label)

        return (
            ModelPrediction(model_name="BETO", prediction=beto_res[0], time_ms=beto_res[1], accuracy=beto_acc, f1_score=beto_f1),
            ModelPrediction(model_name="mBERT", prediction=mbert_res[0], time_ms=mbert_res[1], accuracy=mbert_acc, f1_score=mbert_f1)
        )

    def calculate_metrics(self, predictions: List[int], labels: List[int]) -> Dict[str, float]:
        """
        Calcula métricas de desempeño basándose en predicciones y etiquetas reales.
        """
        if not predictions or not labels or len(predictions) != len(labels):
            return {"accuracy": 0.0, "precision": 0.0, "recall": 0.0, "f1_score": 0.0}

        tp = sum(1 for p, l in zip(predictions, labels) if p == 1 and l == 1)
        fp = sum(1 for p, l in zip(predictions, labels) if p == 1 and l == 0) # Fixed bug here
        fn = sum(1 for p, l in zip(predictions, labels) if p == 0 and l == 1)
        tn = sum(1 for p, l in zip(predictions, labels) if p == 0 and l == 0)

        accuracy = (tp + tn) / len(labels)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score
        }


# Singleton instance
evaluation_service = EvaluationService()
