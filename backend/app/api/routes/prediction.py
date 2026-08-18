from fastapi import APIRouter, HTTPException
from ...schemas.prediction import PredictionRequest, PredictionResponse
from ...services.preprocessing import request_to_dataframe, validate_request, load_allowed_locations
from ...services.inference import model_inference

router = APIRouter(prefix="/api", tags=["prediction"])


@router.get("/health", response_model=dict)
async def health():
    """Health check endpoint."""
    return {"status": "ok", "message": "API is running"}


@router.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Predict house price based on property features.
    
    Returns:
        PredictionResponse with predicted_price in rupees
    """
    
    # Validate request
    is_valid, message = validate_request(request)
    if not is_valid:
        raise HTTPException(status_code=422, detail=message)
    
    try:
        # Convert request to DataFrame
        df = request_to_dataframe(request)
        
        # Make prediction
        predicted_price = model_inference.predict(df)
        
        return PredictionResponse(
            predicted_price=predicted_price,
            message="Prediction successful"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.get("/locations", response_model=list)
async def get_locations():
    """Get list of allowed locations for the form."""
    try:
        locations = load_allowed_locations()
        return locations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load locations: {str(e)}")
