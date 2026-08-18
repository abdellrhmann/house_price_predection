import joblib
import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class ModelInference:
    """Singleton class to manage model loading and inference."""
    
    _instance = None
    _model = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelInference, cls).__new__(cls)
        return cls._instance
    
    def load_model(self, model_path: str):
        """Load the trained model from disk."""
        if self._model is not None:
            return  # Model already loaded
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        try:
            self._model = joblib.load(model_path)
            logger.info(f"✓ Model loaded from {model_path}")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def predict(self, df) -> float:
        """Make a prediction on a single-row DataFrame."""
        if self._model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        try:
            prediction = self._model.predict(df)[0]
            return float(prediction)
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            raise


# Global instance
model_inference = ModelInference()
