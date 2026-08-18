import pandas as pd
import json
import os
from typing import Dict, Any
from ..schemas.prediction import PredictionRequest


def load_allowed_locations() -> list:
    """Load the list of allowed locations from JSON file."""
    locations_file = os.path.join(os.path.dirname(__file__), '../../models/locations.json')
    
    if not os.path.exists(locations_file):
        # Fallback locations if file doesn't exist
        return ['Mumbai', 'Bangalore', 'Delhi', 'Hyderabad', 'Pune', 'other']
    
    with open(locations_file, 'r') as f:
        return json.load(f)


def request_to_dataframe(request: PredictionRequest) -> pd.DataFrame:
    """
    Convert a PredictionRequest to a DataFrame compatible with the trained model.
    Maps unknown locations to 'other'.
    """
    
    allowed_locations = load_allowed_locations()
    
    # Map location: use 'other' if unknown
    location = request.location if request.location in allowed_locations else 'other'
    
    # Create a single-row DataFrame matching training features
    df = pd.DataFrame({
        'location_grouped': [location],
        'carpet_area_sqft': [request.carpet_area_sqft],
        'floor_num': [request.floor_num],
        'Bathroom': [request.bathroom],
        'Balcony': [request.balcony],
        'Furnishing': [request.furnishing],
        'Transaction': [request.transaction],
        'Ownership': [request.ownership],
        'facing': [request.facing],
        'Car Parking': [request.car_parking],
    })
    
    return df


def validate_request(request: PredictionRequest) -> tuple[bool, str]:
    """Validate request data. Returns (is_valid, message)."""
    
    allowed_locations = load_allowed_locations()
    if request.location not in allowed_locations and request.location != 'other':
        # Unknown locations are okay, they'll map to 'other'
        pass
    
    valid_furnishing = ['Unfurnished', 'Semi-Furnished', 'Furnished']
    if request.furnishing not in valid_furnishing:
        return False, f"Invalid furnishing. Must be one of: {', '.join(valid_furnishing)}"
    
    valid_transaction = ['Ready to Move', 'Under Construction']
    if request.transaction not in valid_transaction:
        return False, f"Invalid transaction. Must be one of: {', '.join(valid_transaction)}"
    
    valid_ownership = ['Freehold', 'Leasehold']
    if request.ownership not in valid_ownership:
        return False, f"Invalid ownership. Must be one of: {', '.join(valid_ownership)}"
    
    valid_facing = ['North', 'South', 'East', 'West', 'North-East', 'North-West', 'South-East', 'South-West']
    if request.facing not in valid_facing:
        return False, f"Invalid facing. Must be one of: {', '.join(valid_facing)}"
    
    if request.carpet_area_sqft <= 0:
        return False, "Carpet area must be greater than 0"
    
    if request.bathroom < 0 or request.balcony < 0 or request.car_parking < 0:
        return False, "Bathroom, balcony, and car parking must be >= 0"
    
    return True, "Valid request"
