from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """Request schema for house price prediction."""
    
    location: str = Field(..., description="Location of the property")
    carpet_area_sqft: float = Field(..., gt=0, description="Carpet area in square feet")
    floor_num: int = Field(..., description="Floor number")
    bathroom: int = Field(..., ge=0, description="Number of bathrooms")
    balcony: int = Field(..., ge=0, description="Number of balconies")
    furnishing: str = Field(..., description="Furnishing type: Unfurnished, Semi-Furnished, or Furnished")
    transaction: str = Field(..., description="Transaction type: Ready to Move or Under Construction")
    ownership: str = Field(..., description="Ownership type: Freehold or Leasehold")
    facing: str = Field(..., description="Direction facing: North, South, East, West")
    car_parking: int = Field(default=0, ge=0, description="Number of car parking spaces")


class PredictionResponse(BaseModel):
    """Response schema for house price prediction."""
    
    predicted_price: float = Field(..., description="Predicted house price in rupees")
    message: str = Field(default="Prediction successful", description="Response message")
