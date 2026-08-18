import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.inference import model_inference
import os

# Load model before tests
@pytest.fixture(scope="session", autouse=True)
def load_model():
    """Load model once for all tests."""
    model_path = os.path.join(os.path.dirname(__file__), '../models/house_price.pkl')
    if os.path.exists(model_path):
        model_inference.load_model(model_path)


client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict_valid_input():
    """Test prediction with valid input."""
    request_data = {
        "location": "Mumbai",
        "carpet_area_sqft": 1200,
        "floor_num": 5,
        "bathroom": 2,
        "balcony": 1,
        "furnishing": "Furnished",
        "transaction": "Ready to Move",
        "ownership": "Freehold",
        "facing": "North",
        "car_parking": 1
    }
    
    response = client.post("/api/predict", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "predicted_price" in data
    assert isinstance(data["predicted_price"], (int, float))
    assert data["predicted_price"] > 0
    print(f"✓ Prediction: ₹{data['predicted_price']:,.0f}")


def test_predict_invalid_furnishing():
    """Test prediction with invalid furnishing type (should fail)."""
    request_data = {
        "location": "Mumbai",
        "carpet_area_sqft": 1200,
        "floor_num": 5,
        "bathroom": 2,
        "balcony": 1,
        "furnishing": "InvalidFurnishing",  # This is invalid
        "transaction": "Ready to Move",
        "ownership": "Freehold",
        "facing": "North",
        "car_parking": 1
    }
    
    response = client.post("/api/predict", json=request_data)
    assert response.status_code == 422  # Validation error


def test_predict_negative_area():
    """Test prediction with negative carpet area (should fail)."""
    request_data = {
        "location": "Mumbai",
        "carpet_area_sqft": -100,  # Invalid
        "floor_num": 5,
        "bathroom": 2,
        "balcony": 1,
        "furnishing": "Furnished",
        "transaction": "Ready to Move",
        "ownership": "Freehold",
        "facing": "North",
        "car_parking": 1
    }
    
    response = client.post("/api/predict", json=request_data)
    assert response.status_code == 422


def test_locations_endpoint():
    """Test locations list endpoint."""
    response = client.get("/api/locations")
    assert response.status_code == 200
    
    locations = response.json()
    assert isinstance(locations, list)
    assert len(locations) > 0
    assert 'other' in locations or len(locations) > 0
    print(f"✓ Available locations: {len(locations)}")


def test_unknown_location_maps_to_other():
    """Test that unknown location is handled gracefully (maps to 'other')."""
    request_data = {
        "location": "UnknownCity123",
        "carpet_area_sqft": 1200,
        "floor_num": 5,
        "bathroom": 2,
        "balcony": 1,
        "furnishing": "Furnished",
        "transaction": "Ready to Move",
        "ownership": "Freehold",
        "facing": "North",
        "car_parking": 1
    }
    
    response = client.post("/api/predict", json=request_data)
    assert response.status_code == 200  # Should succeed, mapping to 'other'
    data = response.json()
    assert "predicted_price" in data
    print(f"✓ Unknown location handled (mapped to 'other'): ₹{data['predicted_price']:,.0f}")
