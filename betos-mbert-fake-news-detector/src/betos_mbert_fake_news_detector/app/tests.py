"""
Unit tests for Fake News Detection API

This module contains unit tests for the core functionality of the
BETO and mBERT model comparison platform.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

from .main import app, service

client = TestClient(app)

class TestService:
    """Test the service layer"""
    
    def test_calculate_metrics(self):
        """Test metrics calculation function"""
        from .services.service import EvaluationService
        
        service_instance = EvaluationService()
        
        # Test with perfect predictions
        predictions = [1, 0, 1, 0]
        labels = [1, 0, 1, 0]
        metrics = service_instance.calculate_metrics(predictions, labels)
        
        assert metrics.accuracy == 1.0
        assert metrics.precision == 1.0
        assert metrics.recall == 1.0
        assert metrics.f1_score == 1.0
        
        # Test with no predictions
        metrics = service_instance.calculate_metrics([], [])
        assert metrics.accuracy == 0.0
        assert metrics.precision == 0.0
        assert metrics.recall == 0.0
        assert metrics.f1_score == 0.0
    
    @pytest.mark.asyncio
    async def test_evaluate_text(self):
        """Test text evaluation function"""
        from .services.service import EvaluationService
        
        service_instance = EvaluationService()
        
        # Mock the model inference functions
        with patch.object(service_instance, 'mock_beto_inference', new_callable=AsyncMock) as mock_beto, \
             patch.object(service_instance, 'mock_mbert_inference', new_callable=AsyncMock) as mock_mbert:
            
            mock_beto.return_value = (1, 0.1)
            mock_mbert.return_value = (0, 0.15)
            
            result = await service_instance.evaluate_text("Test text", 1)
            
            assert result.text == "Test text"
            assert result.label == 1
            assert result.beto_prediction == 1
            assert result.mbert_prediction == 0
            assert result.beto_time_ms == 0.1
            assert result.mbert_time_ms == 0.15
            assert result.beto_accuracy == 1.0
            assert result.mbert_accuracy == 0.0

class TestAPI:
    """Test the API endpoints"""
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
    
    def test_evaluate_endpoint(self):
        """Test evaluate endpoint"""
        response = client.post(
            "/api/v1/evaluate",
            json={"text": "This is a test text", "label": 1}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["text"] == "This is a test text"
        assert data["label"] == 1
        assert "beto_prediction" in data
        assert "mbert_prediction" in data
        assert "beto_time_ms" in data
        assert "mbert_time_ms" in data
    
    def test_evaluate_endpoint_validation_error(self):
        """Test evaluate endpoint with invalid data"""
        response = client.post(
            "/api/v1/evaluate",
            json={"text": ""}  # Empty text should cause validation error
        )
        assert response.status_code == 422
    
    def test_batch_evaluate_endpoint(self):
        """Test batch evaluate endpoint"""
        response = client.post(
            "/api/v1/dataset/evaluate",
            json={
                "texts": ["Test text 1", "Test text 2"],
                "labels": [1, 0]
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["text"] == "Test text 1"
        assert data[1]["text"] == "Test text 2"
    
    def test_reports_metrics_endpoint(self):
        """Test reports metrics endpoint"""
        response = client.get("/api/v1/reports/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "total_evaluations" in data
        assert "beto_metrics" in data
        assert "mbert_metrics" in data
        assert "comparison" in data
        assert "latest_evaluation" in data
    
    def test_export_results_endpoint(self):
        """Test export results endpoint"""
        response = client.get("/api/v1/results/export")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_integration_workflow(self):
        """Test a complete workflow: evaluate -> batch evaluate -> get metrics -> export"""
        # Test single text evaluation
        response = client.post(
            "/api/v1/evaluate",
            json={"text": "Integration test text", "label": 1}
        )
        assert response.status_code == 200
        single_result = response.json()
        
        # Test batch evaluation
        response = client.post(
            "/api/v1/dataset/evaluate",
            json={
                "texts": ["Batch test 1", "Batch test 2"],
                "labels": [0, 1]
            }
        )
        assert response.status_code == 200
        batch_results = response.json()
        assert len(batch_results) == 2
        
        # Test metrics report
        response = client.get("/api/v1/reports/metrics")
        assert response.status_code == 200
        metrics = response.json()
        assert metrics["total_evaluations"] >= 3  # 1 single + 2 batch
        
        # Test export
        response = client.get("/api/v1/results/export")
        assert response.status_code == 200
        export_results = response.json()
        assert len(export_results) >= 3
    
    def test_performance_batch_evaluation(self):
        """Test performance of batch evaluation endpoint"""
        import time
        
        # Create a large batch of texts
        large_batch = [f"Test text {i}" for i in range(100)]
        
        # Measure time for batch evaluation
        start_time = time.time()
        response = client.post(
            "/api/v1/dataset/evaluate",
            json={"texts": large_batch, "labels": [1] * 100}
        )
        end_time = time.time()
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 100
        
        # Performance should be reasonable (less than 30 seconds for 100 texts)
        processing_time = end_time - start_time
        assert processing_time < 30.0, f"Batch processing took too long: {processing_time:.2f} seconds"
    
    def test_error_handling(self):
        """Test error handling for various error scenarios"""
        # Test with invalid JSON
        response = client.post(
            "/api/v1/evaluate",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        # Should return 422 or 400 for validation error
        assert response.status_code in [400, 422]
        
        # Test with missing required field
        response = client.post(
            "/api/v1/evaluate",
            json={"label": 1}  # Missing text field
        )
        assert response.status_code == 422

    def test_performance_with_large_dataset(self):
        """Test performance with a large dataset"""
        import time
        
        # Create a large batch of texts
        large_batch = [f"Test text {i} with some content to make it realistic" for i in range(500)]
        
        # Measure time for batch evaluation
        start_time = time.time()
        response = client.post(
            "/api/v1/dataset/evaluate",
            json={"texts": large_batch, "labels": [1] * 500}
        )
        end_time = time.time()
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 500
        
        # Performance should be reasonable (less than 60 seconds for 500 texts)
        processing_time = end_time - start_time
        assert processing_time < 60.0, f"Large batch processing took too long: {processing_time:.2f} seconds"

    def test_concurrent_requests(self):
        """Test handling of concurrent requests"""
        import threading
        import time
        
        results = []
        errors = []
        
        def make_request(text_id):
            try:
                response = client.post(
                    "/api/v1/evaluate",
                    json={"text": f"Concurrent test text {text_id}", "label": text_id % 2}
                )
                results.append(response.status_code)
            except Exception as e:
                errors.append(str(e))
        
        # Create multiple threads to simulate concurrent requests
        threads = []
        for i in range(10):
            thread = threading.Thread(target=make_request, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check that all requests were successful
        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert all(status == 200 for status in results), f"Some requests failed: {results}"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
