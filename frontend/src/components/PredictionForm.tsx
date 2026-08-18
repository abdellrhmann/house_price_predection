import React, { useState, useEffect } from 'react';
import { FormData } from '../types/prediction';
import { fetchLocations, predictPrice } from '../api/predictionClient';
import '../styles/form.css';

interface PredictionFormProps {
  onPredict: (predictedPrice: number) => void;
  onLoading: (isLoading: boolean) => void;
  onError: (error: string) => void;
}

export const PredictionForm: React.FC<PredictionFormProps> = ({
  onPredict,
  onLoading,
  onError,
}) => {
  const [locations, setLocations] = useState<string[]>([]);
  const [formData, setFormData] = useState<FormData>({
    location: '',
    carpet_area_sqft: 0,
    floor_num: 0,
    bathroom: 1,
    balcony: 0,
    furnishing: 'Unfurnished',
    transaction: 'Ready to Move',
    ownership: 'Freehold',
    facing: 'North',
    car_parking: 0,
  });
  const [errors, setErrors] = useState<Record<string, string>>({});

  // Load locations on mount
  useEffect(() => {
    const loadLocations = async () => {
      try {
        const locs = await fetchLocations();
        setLocations(locs);
        if (locs.length > 0) {
          setFormData((prev) => ({ ...prev, location: locs[0] }));
        }
      } catch (err) {
        onError('Failed to load locations');
        console.error(err);
      }
    };
    loadLocations();
  }, [onError]);

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.location) {
      newErrors.location = 'Location is required';
    }
    if (formData.carpet_area_sqft <= 0) {
      newErrors.carpet_area_sqft = 'Area must be greater than 0';
    }
    if (formData.bathroom < 0) {
      newErrors.bathroom = 'Bathrooms cannot be negative';
    }
    if (formData.balcony < 0) {
      newErrors.balcony = 'Balconies cannot be negative';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    const numValue = ['carpet_area_sqft', 'floor_num', 'bathroom', 'balcony', 'car_parking'].includes(
      name
    )
      ? parseFloat(value)
      : value;

    setFormData((prev) => ({
      ...prev,
      [name]: numValue,
    }));

    // Clear error for this field
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    onLoading(true);
    onError('');

    try {
      const response = await predictPrice(formData);
      onPredict(response.predicted_price);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Prediction failed. Please try again.';
      onError(errorMsg);
    } finally {
      onLoading(false);
    }
  };

  return (
    <form className="prediction-form" onSubmit={handleSubmit}>
      <h2>Predict House Price</h2>

      <div className="form-group">
        <label htmlFor="location">Location *</label>
        <select
          id="location"
          name="location"
          value={formData.location}
          onChange={handleChange}
          className={errors.location ? 'error' : ''}
          required
        >
          <option value="">Select location</option>
          {locations.map((loc) => (
            <option key={loc} value={loc}>
              {loc}
            </option>
          ))}
        </select>
        {errors.location && <span className="error-text">{errors.location}</span>}
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="carpet_area_sqft">Carpet Area (sqft) *</label>
          <input
            type="number"
            id="carpet_area_sqft"
            name="carpet_area_sqft"
            value={formData.carpet_area_sqft || ''}
            onChange={handleChange}
            className={errors.carpet_area_sqft ? 'error' : ''}
            placeholder="e.g., 1200"
            min="1"
            step="10"
            required
          />
          {errors.carpet_area_sqft && (
            <span className="error-text">{errors.carpet_area_sqft}</span>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="floor_num">Floor Number</label>
          <input
            type="number"
            id="floor_num"
            name="floor_num"
            value={formData.floor_num}
            onChange={handleChange}
            placeholder="e.g., 3"
            step="1"
          />
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="bathroom">Bathrooms</label>
          <input
            type="number"
            id="bathroom"
            name="bathroom"
            value={formData.bathroom}
            onChange={handleChange}
            min="0"
            step="1"
          />
        </div>

        <div className="form-group">
          <label htmlFor="balcony">Balconies</label>
          <input
            type="number"
            id="balcony"
            name="balcony"
            value={formData.balcony}
            onChange={handleChange}
            min="0"
            step="1"
          />
        </div>

        <div className="form-group">
          <label htmlFor="car_parking">Car Parking</label>
          <input
            type="number"
            id="car_parking"
            name="car_parking"
            value={formData.car_parking}
            onChange={handleChange}
            min="0"
            step="1"
          />
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="furnishing">Furnishing</label>
          <select
            id="furnishing"
            name="furnishing"
            value={formData.furnishing}
            onChange={handleChange}
          >
            <option value="Unfurnished">Unfurnished</option>
            <option value="Semi-Furnished">Semi-Furnished</option>
            <option value="Furnished">Furnished</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="transaction">Transaction Type</label>
          <select
            id="transaction"
            name="transaction"
            value={formData.transaction}
            onChange={handleChange}
          >
            <option value="Ready to Move">Ready to Move</option>
            <option value="Under Construction">Under Construction</option>
          </select>
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="ownership">Ownership</label>
          <select
            id="ownership"
            name="ownership"
            value={formData.ownership}
            onChange={handleChange}
          >
            <option value="Freehold">Freehold</option>
            <option value="Leasehold">Leasehold</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="facing">Facing Direction</label>
          <select
            id="facing"
            name="facing"
            value={formData.facing}
            onChange={handleChange}
          >
            <option value="North">North</option>
            <option value="South">South</option>
            <option value="East">East</option>
            <option value="West">West</option>
            <option value="North-East">North-East</option>
            <option value="North-West">North-West</option>
            <option value="South-East">South-East</option>
            <option value="South-West">South-West</option>
          </select>
        </div>
      </div>

      <button type="submit" className="btn-predict">
        Predict Price
      </button>
    </form>
  );
};
