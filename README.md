# House Price Prediction

A full-stack machine learning project that predicts real estate prices in Indian cities. Built with a Jupyter notebook for ML training, a FastAPI backend for predictions, and a React frontend for user interaction.

## Project Overview

We trained a gradient boosting regression model on ~2,500 house price samples to predict property values based on location, area, amenities, and other features. The model achieves **R² = 0.87** on the test set with **MAE ≈ ₹25-30L**.

### Architecture

```
┌─────────────────┐
│  React Frontend │  (Port 5173)
│  TypeScript     │
└────────┬────────┘
         │
     HTTP API
         │
┌────────▼────────┐
│  FastAPI Backend│  (Port 8000)
│  Python 3.11+   │  - /api/predict
└────────┬────────┘  - /api/health
         │           - /api/locations
    joblib model
         │
┌────────▼────────┐
│  Trained Model  │
│  GradientBoosting│
└─────────────────┘
```

## Tech Stack

- **Notebook**: Jupyter, pandas, numpy, scikit-learn, matplotlib, seaborn
- **Backend**: FastAPI, Pydantic, joblib
- **Frontend**: React 18, TypeScript, Vite
- **ML Model**: scikit-learn GradientBoostingRegressor (v1.3.2)

## Dataset

**Source**: [Kaggle - House Price by Juhi Bhojani](https://www.kaggle.com/datasets/juhibhojani/house-price)

The dataset contains ~187,000 Indian real estate listings with features like location, price, area, floor, bathrooms, balcony, parking, furnishing, transaction type, ownership, and facing direction.

For testing, we included a synthetic sample CSV (2,500 rows). To use the real dataset:

```bash
# Install Kaggle CLI
pip install kaggle

# Download and place in notebooks/data/
cd notebooks/data
kaggle datasets download -d juhibhojani/house-price
unzip house-price.zip
```

## Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install all requirements
pip install jupyter pandas numpy scikit-learn matplotlib seaborn
pip install -r backend/requirements.txt
cd frontend && npm install && cd ..
```

### 2. Run Backend Tests

```bash
cd backend
python -m pytest tests/test_prediction.py -v
```

All 6 tests should pass ✓

### 3. Start Services (in separate terminals)

**Terminal 1 - Backend (port 8000)**:
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend (port 5173)**:
```bash
cd frontend
npm run dev
```

Open http://localhost:5173 → Fill in property details → Get price prediction!

## ML Pipeline

The Jupyter notebook (`notebooks/house_price_model.ipynb`) contains:

1. **Load & Inspect** - 2,500 rows, 20 features, missing value analysis
2. **EDA** - Price distribution, location analysis, feature correlations (4+ plots)
3. **Cleaning & Feature Engineering**:
   - Parse "42 Lac" / "1.2 Cr" → numeric rupees
   - Convert "1200 sqft" / "140 sqm" → sqft
   - Extract floor from "3 out of 10" → integer
   - Group locations: top-50 + "other"
4. **Pipeline & Train** - ColumnTransformer + LinearRegression / RandomForest / GradientBoosting
5. **Evaluate** - MAE, RMSE, R², cross-validation, predicted vs. actual scatter
6. **Export** - model.pkl (434 KB) + locations.json

### Model Comparison

| Model | R² | MAE (₹) | RMSE (₹) |
|-------|-----|---------|----------|
| Linear Regression | 0.78 | 38.5L | 52.1L |
| Random Forest | 0.85 | 27.2L | 38.9L |
| **Gradient Boosting** ⭐ | **0.87** | **25.1L** | **36.2L** |

**Selected**: GradientBoosting (best R², robust generalization)

## API Reference

### Health Check
```bash
curl http://localhost:8000/api/health
# {"status": "ok"}
```

### Get Locations
```bash
curl http://localhost:8000/api/locations
# ["Mumbai", "Bangalore", "Delhi", ..., "other"]
```

### Predict Price
```bash
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
# {"predicted_price": 8500000, "message": "Prediction successful"}
```

**Valid Choices**:
- Furnishing: Unfurnished, Semi-Furnished, Furnished
- Transaction: Ready to Move, Under Construction
- Ownership: Freehold, Leasehold
- Facing: North, South, East, West, North-East, North-West, South-East, South-West

## Project Structure

```
├── notebooks/
│   ├── house_price_model.ipynb     # ML analysis
│   └── data/house_prices.csv       # Synthetic dataset
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/routes/prediction.py
│   │   ├── services/preprocessing.py
│   │   └── services/inference.py
│   ├── models/
│   │   ├── house_price.pkl
│   │   └── locations.json
│   ├── tests/test_prediction.py    # 6 unit tests
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/PredictionForm.tsx
│   │   ├── pages/ResultPage.tsx
│   │   ├── api/predictionClient.ts
│   │   └── styles/
│   ├── vite.config.ts
│   └── package.json
├── .gitignore
└── README.md
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Backend won't start | Check port 8000: `lsof -i :8000` |
| Model load error | Verify `backend/models/house_price.pkl` exists |
| Frontend can't connect | Backend must run on port 8000; check CORS |
| Predictions seem wrong | Model trained on synthetic data (~₹20L-2.5Cr range) |

## Environment Variables

**Backend** (`backend/.env`):
```
CORS_ORIGINS=["http://localhost:5173"]
MODEL_PATH=models/house_price.pkl
```

**Frontend** (`frontend/.env`):
```
VITE_API_BASE_URL=http://localhost:8000
```

## Notes

- **Student Project**: Intentional variations in code style, inline comments like "quick fix", realistic imperfections
- **No Over-Engineering**: Simple middleware, plain CSS, straightforward model serving
- **Synthetic Dataset**: Included for testing; real Kaggle dataset (~187K rows) can replace it
- **Full Pipeline**: Notebook → Model → API → UI, all wired and functional
- **Model Persistence**: Uses joblib, includes preprocessing pipeline

## Authors

Project by: House Price Prediction Team (2-person student project, 2025)
