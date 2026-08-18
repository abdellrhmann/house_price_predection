from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

from app.core.config import get_settings
from app.api.routes import prediction
from app.services.inference import model_inference

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager: load model on startup, cleanup on shutdown.
    """
    # Startup
    logger.info("Starting up...")
    settings = get_settings()
    
    # Resolve model path (relative to app directory or absolute)
    if os.path.isabs(settings.model_path):
        model_path = settings.model_path
    else:
        # Assume model_path is relative to the backend directory
        model_path = os.path.join(os.path.dirname(__file__), '../../' + settings.model_path)
        model_path = os.path.abspath(model_path)
    
    try:
        model_inference.load_model(model_path)
        logger.info(f"✓ Model loaded: {model_path}")
    except Exception as e:
        logger.error(f"Failed to load model during startup: {e}")
        raise
    
    yield  # App runs here
    
    # Shutdown
    logger.info("Shutting down...")


# Create app
app = FastAPI(
    title=get_settings().app_name,
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(prediction.router)


@app.get("/")
async def root():
    """Root endpoint - API documentation is at /docs"""
    return {
        "message": "House Price Prediction API",
        "docs": "/docs",
        "health": "/api/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
